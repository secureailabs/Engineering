import logging
from typing import Optional, Union

import msgpack
import zmq
import zmq.asyncio

from zero.errors import MethodNotFoundException, ZeroException

# public_keys_dir = "/home/jjj/ScratchPad/JingweiZhang/prefect_related/public_keys/"
# private_keys_dir = "/home/jjj/ScratchPad/JingweiZhang/prefect_related/private_keys/"
public_keys_dir = "/app/public_keys/"
private_keys_dir = "/app/private_keys/"


class _BaseClient:
    def __init__(
        self,
        host: str,
        port: int,
        default_timeout: int = 2000,
    ):
        self._host = host
        self._port = port
        self._default_timeout = default_timeout
        self._serializer = "msgpack"
        self._init_serializer()
        self._socket: Optional[zmq.Socket] = None

    def _init_serializer(self):
        # msgpack is the default serializer
        if self._serializer == "msgpack":
            self._encode = msgpack.packb
            self._decode = msgpack.unpackb

    def _set_socket_opt(self):
        self._socket.setsockopt(zmq.RCVTIMEO, self._default_timeout)
        self._socket.setsockopt(zmq.SNDTIMEO, self._default_timeout)
        self._socket.setsockopt(zmq.LINGER, 0)  # dont buffer messages


class ZeroClient(_BaseClient):
    def __init__(
        self,
        host: str,
        port: int,
        default_timeout: int = 2000,
    ):
        """
        ZeroClient provides the client interface for calling the ZeroServer.

        @param host:
        Host of the ZeroServer.

        @param port:
        Port of the ZeroServer.

        @param default_timeout:
        Default timeout for each call. In milliseconds.
        """
        super().__init__(host, port, default_timeout)

    def _init_socket(self):
        ctx = zmq.Context.instance()
        self._socket: zmq.Socket = ctx.socket(zmq.DEALER)

        client_secret_file = private_keys_dir + "client.key_secret"
        client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
        self._socket.curve_secretkey = client_secret
        self._socket.curve_publickey = client_public

        server_public_file = public_keys_dir + "server.key"
        server_public, _ = zmq.auth.load_certificate(server_public_file)
        self._socket.curve_serverkey = server_public

        self._set_socket_opt()
        res = self._socket.connect(f"tcp://{self._host}:{self._port}")
        print(res)

    # outgoing message:
    # 0->function call
    # 1->constructor call
    # 2->attribute call
    # 3->method call
    # 4->destructor call
    # incoming message:
    # 0->exception
    # 1->secret object
    # 2->secret object as a proxy
    def _send_msg(self, msg, msg_type):
        if self._socket is None:
            self._init_socket()

        try:
            self._socket.send_multipart([self._encode(msg_type), self._encode(msg)], zmq.DONTWAIT)
            resp = self._socket.recv()
            decoded_resp = self._decode(resp, use_list=False, strict_map_key=False)
            decoded_resp = self._process_resp(decoded_resp)
            print(decoded_resp)

            # if isinstance(decoded_resp, dict):
            #     if "__zerror__method_not_found" in decoded_resp:
            #         raise MethodNotFoundException(decoded_resp.get("__zerror__method_not_found"))
            #     elif "__Exception" in decoded_resp:
            #         raise Exception(decoded_resp["Message"])
            #     elif "_SecretClientObject" in decoded_resp:
            #        decoded_resp["client"] = self
            return decoded_resp
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                pass  # no message was ready (yet!)
        except ZeroException as ze:
            raise ze
        except Exception as e:
            self._socket.close()
            self._init_socket()
            # logging.exception(e)
            raise

    def _process_resp(self, msg):
        resp = None
        if isinstance(msg, tuple):
            tmp_list = list(tuple)
            for i in range(len(list)):
                tmp_list[i] = self._precess_resp(tmp_list[i])
            resp = tuple(tmp_list)
        elif isinstance(msg, dict) and "object" in msg:
            if msg["object"] == 0:
                raise Exception(msg["Message"])
            elif msg["object"] == 1:
                resp = Proxy(msg["id"], msg["type"], self)
            elif msg["object"] == 2:
                resp = msg
            else:
                raise Exception("unknown return object from remote end")
        else:
            resp = msg
        return resp

    def call(self, rpc_method_name, *args, **kwargs):
        """
        Call the rpc method of the ZeroServer.

        @param rpc_method_name:
        Method name should be string. This method should reside on the ZeroServer to get a successful response.

        @param msg:
        For msgpack serializer, msg should be base Python types. Cannot be objects.

        @return:
        Returns the response of ZeroServer's rpc method.
        """
        msg_type = 0
        msg = {}
        msg["function_name"] = rpc_method_name
        msg["vargs"] = args
        msg["kwargs"] = kwargs
        return self._send_msg(msg, msg_type)

    def proxy(self, ro_name, *args, **kwargs):
        msg_type = 1
        msg = {}
        msg["vargs"] = args
        msg["kwargs"] = kwargs
        msg["class_name"] = ro_name
        sec_obj = self._send_msg(msg, msg_type)
        return Proxy(sec_obj["id"], sec_obj["type"], self)


class AsyncZeroClient(_BaseClient):
    def __init__(
        self,
        host: str,
        port: int,
        default_timeout: int = 2000,
    ):
        """
        AsyncZeroClient provides the asynchronous client interface for calling the ZeroServer.
        You can use Python's async/await with this client.
        Naturally async client is faster.

        @param host:
        Host of the ZeroServer.

        @param port:
        Port of the ZeroServer.

        @param default_timeout:
        Default timeout for each call. In milliseconds.
        """
        super().__init__(host, port, default_timeout)

    def _init_async_socket(self):
        ctx = zmq.asyncio.Context.instance()
        self._socket: zmq.Socket = ctx.socket(zmq.DEALER)
        self._set_socket_opt()
        self._socket.connect(f"tcp://{self._host}:{self._port}")

    async def call(self, rpc_method_name: str, msg: Union[int, float, str, dict, list, tuple, None]):
        """
        Call the rpc method of the ZeroServer.

        @param rpc_method_name:
        Method name should be string. This method should reside on the ZeroServer to get a successful response.

        @param msg:
        For msgpack serializer, msg should be base Python types. Cannot be objects.

        @return:
        Returns the response of ZeroServer's rpc method.
        """
        if self._socket is None:
            self._init_async_socket()
        try:
            msg = "" if msg is None else msg
            await self._socket.send_multipart([rpc_method_name.encode(), self._encode(msg)], zmq.DONTWAIT)
            resp = await self._socket.recv()
            decoded_resp = self._decode(resp)
            if isinstance(decoded_resp, dict):
                if "__zerror__method_not_found" in decoded_resp:
                    raise MethodNotFoundException(decoded_resp.get("__zerror__method_not_found"))
            return decoded_resp
        except ZeroException as ze:
            raise ze
        except Exception as e:
            self._socket.close()
            self._init_async_socket()
            logging.exception(e)


class Proxy(object):
    __roAttributes = frozenset(
        ["_roid", "_rotype", "_roMethods", "_roAttrs", "_client", "_roInvoke", "_roGetMetadata", "__processMetadata"]
    )

    def __init__(self, object_id, object_type, client):
        self._roid = object_id
        self._rotype = object_type
        self._roMethods = set()  # all methods of the remote object, gotten from meta-data
        self._roAttrs = set()  # attributes of the remote object, gotten from meta-data
        self._client = client
        # self._pyroSeq = 0  # message sequence number
        # self._pyroRawWireResponse = False  # internal switch to enable wire level responses

    def __del__(self):
        ##send a signal to remote end to delete stored object
        msg_type = 4
        msg = {}
        msg["object_id"] = self._roid
        self._client._send_msg(msg, msg_type)

    def __getattr__(self, name):
        # get metadata if it's not there yet
        if name in Proxy.__roAttributes:
            raise AttributeError(name)
        if not self._roMethods and not self._roAttrs:
            self._roGetMetadata()
        if name in self._roAttrs:
            return self._roInvoke("__getattribute__", (name,), None)
        if name not in self._roMethods:
            # client side check if the requested attr actually exists
            raise AttributeError("remote object '%s' has no exposed attribute or method '%s'" % (self._pyroUri, name))
        return _RemoteMethod(self._roInvoke, name)

    def __setattr__(self, name, value):
        if name in Proxy.__roAttributes:
            return super(Proxy, self).__setattr__(name, value)  # one of the special pyro attributes
        # get metadata if it's not there yet
        if not self._roMethods and not self._roAttrs:
            self._roGetMetadata()
        if name in self._pyroAttrs:
            return self._roInvoke("__setattr__", (name, value), None)  # remote attribute
        # client side validation if the requested attr actually exists
        raise AttributeError("remote object '%s' has no exposed attribute '%s'" % (self._pyroUri, name))

    def __copy__(self):
        p = object.__new__(type(self))
        p._roid = self._roid
        p._roMethods = self._roMethods
        p._roAttrs = self._roAttrs
        return p

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __eq__(self, other):
        if other is self:
            return True
        return isinstance(other, Proxy) and other._roid == self._roid

    def __ne__(self, other):
        if other and isinstance(other, Proxy):
            return other._roid != self._roid
        return True

    def __hash__(self):
        return hash(self._roid)

    def __dir__(self):
        result = dir(self.__class__) + list(self.__dict__.keys())
        return sorted(set(result) | self._roMethods | self._roAttrs)

    # When special methods are invoked via special syntax (e.g. obj[index] calls
    # obj.__getitem__(index)), the special methods are not looked up via __getattr__
    # for efficiency reasons; instead, their presence is checked directly.
    # Thus we need to define them here to force (remote) lookup through __getitem__.
    def __bool__(self):
        return True

    def __len__(self):
        return self.__getattr__("__len__")()

    def __getitem__(self, index):
        return self.__getattr__("__getitem__")(index)

    def __setitem__(self, index, val):
        return self.__getattr__("__setitem__")(index, val)

    def __delitem__(self, index):
        return self.__getattr__("__delitem__")(index)

    def __iter__(self):
        try:
            # use remote iterator if it exists
            yield from self.__getattr__("__iter__")()
        except AttributeError:
            # fallback to indexed based iteration
            try:
                yield from (self[index] for index in range(sys.maxsize))
            except (StopIteration, IndexError):
                return

    def _roInvoke(self, methodname, vargs, kwargs):

        msg_type = 3
        msg = {}
        msg["object_id"] = self._roid
        msg["method_name"] = methodname
        msg["vargs"] = vargs
        msg["kwargs"] = kwargs

        return self._client._send_msg(msg, msg_type)

    def _roGetMetadata(self):

        if self._roMethods or self._roAttrs:
            return  # metadata has already been retrieved as part of creating the connection

        try:
            # invoke the get_metadata method on the daemon
            msg_type = 2
            msg = {}
            msg["object_id"] = self._roid
            result = self._client._send_msg(msg, msg_type)
            self.__processMetadata(result)
        except ZeroException:
            logging.exception("problem getting metadata")
            raise

    def __processMetadata(self, metadata):
        if not metadata:
            return
        self._roMethods = set(metadata["methods"])
        self._roAttrs = set(metadata["attributes"])
        # if logging.isEnabledFor(logging.DEBUG):
        #     logging.debug(
        #         "from meta: methods=%s, oneway methods=%s, attributes=%s",
        #         sorted(self._roMethods),
        #         sorted(self._roAttrs),
        #     )
        if not self._roMethods and not self._roAttrs:
            raise ZeroException(
                "remote object doesn't expose any methods or attributes. Did you forget setting @expose on them?"
            )


class _RemoteMethod(object):
    """method call abstraction"""

    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _RemoteMethod(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args, **kwargs):
        return self.__send(self.__name, args, kwargs)