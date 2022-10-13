# -------------------------------------------------------------------------------
# Engineering
# client.py
# -------------------------------------------------------------------------------
"""RPC client side module"""
# -------------------------------------------------------------------------------
# modified from https://github.com/Ananto30/zero under MIT license
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import logging
import sys
from typing import Optional, Union

import msgpack
import zmq
import zmq.asyncio

from zero.errors import MethodNotFoundException, ZeroException
from zero.serialize import deserializer_table, serializer_table

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
        """
        Client class for orchestrator

        :param host: host ip
        :type host: str
        :param port: host port to connect
        :type port: int
        :param default_timeout: _description_, defaults to 2000
        :type default_timeout: int, optional
        """
        self._host = host
        self._port = port
        self._default_timeout = default_timeout
        self._serializer = "msgpack"
        self._init_serializer()
        self._socket: Optional[zmq.Socket] = None

    def _init_serializer(self):
        """
        initialize serializer
        msgpack is the default serializer
        """
        if self._serializer == "msgpack":
            self._encode = msgpack.packb
            self._decode = msgpack.unpackb

    def _set_socket_opt(self):
        """
        set socket parameters
        """
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
        """
        Initialize socket with TLS keys
        """
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
        self._socket.connect(f"tcp://{self._host}:{self._port}")

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
        """
        send message from client to server

        :param msg: message payload
        :type msg: dict
        :param msg_type: message type
        :type msg_type: int
        :raises ze: raise when there is a connection error on zmq layer
        :return: response from server
        :rtype: Any
        """
        if self._socket is None:
            self._init_socket()

        try:
            self._socket.send_multipart([self._encode(msg_type), self._encode(msg)], zmq.DONTWAIT)
            resp = self._socket.recv()
            decoded_resp = self._decode(resp, use_list=False, strict_map_key=False)
            decoded_resp = self._process_resp(decoded_resp)

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
            raise e

    def _process_args(self, args, kwargs):
        """
        process arguments of the rpc call

        :param args: variable args
        :type args: tuple
        :param kwargs: keyword args
        :type kwargs: dict
        :return: args and kwargs after processed
        :rtype: tuple
        """
        if args is not None:
            args = list(args)
            for i in range(len(args)):
                if isinstance(args[i], Proxy):
                    args[i] = serializer_table["proxy"](args[i])
            args = tuple(args)
        if kwargs is not None:
            for k, v in kwargs:
                if isinstance(v, Proxy):
                    kwargs[k] = serializer_table["proxy"](v)
        return args, kwargs

    def _process_resp(self, msg):
        """
        process response message

        :param msg: response message
        :type msg: Any
        :raises Exception: unknown return object
        :return: processed message
        :rtype: Any
        """
        resp = None
        if isinstance(msg, tuple):
            tmp_list = list(msg)
            for i in range(len(tmp_list)):
                tmp_list[i] = self._process_resp(tmp_list[i])
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
        elif isinstance(msg, dict) and "__type__" in msg:
            resp = deserializer_table[msg["__type__"]](msg)
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
        args, kwargs = self._process_args(args, kwargs)
        msg["function_name"] = rpc_method_name
        msg["vargs"] = args
        msg["kwargs"] = kwargs
        return self._send_msg(msg, msg_type)

    def proxy(self, ro_name, *args, **kwargs):
        """
        create a proxy mirror image of a remote object

        :param ro_name: remote object class name
        :type ro_name: str
        :return: proxy mirror image
        :rtype: Proxy
        """
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
        """
        Initialize asynchronous socket
        """
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
        [
            "_roid",
            "_rotype",
            "_roMethods",
            "_roAttrs",
            "_client",
            "_roInvoke",
            "_roGetMetadata",
            "__processMetadata",
        ]
    )

    def __init__(self, object_id, object_type, client):
        """
        Proxy class from remote object

        :param object_id: remote object id
        :type object_id: str
        :param object_type: remote object type
        :type object_type: str
        :param client: which client does the proxy object belongs to
        :type client: _BaseClient
        """
        self._roid = object_id
        self._rotype = object_type
        self._roMethods = set()  # all methods of the remote object, gotten from meta-data
        self._roAttrs = set()  # attributes of the remote object, gotten from meta-data
        self._client = client
        # self._pyroSeq = 0  # message sequence number
        # self._pyroRawWireResponse = False  # internal switch to enable wire level responses

    # def __del__(self):
    #    """
    #    destructor call will send a signal to remote end to delete stored object
    #    """
    #    msg_type = 4
    #   msg = {}
    #    msg["object_id"] = self._roid
    #    self._client._send_msg(msg, msg_type)

    def __getattr__(self, name):
        """
        get attribute from remote object

        :param name: attribute name
        :type name: str
        :raises AttributeError: there is no such attribute on the remote end
        :return: the attribute value
        :rtype: Any
        """
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
        """
        set attribute value on the remote end

        :param name: attribute name
        :type name: str
        :param value: new value to be assigned to the attribute
        :type value: Any
        :raises AttributeError: No such attribute for remote object
        :return: None
        :rtype: None
        """
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
        """
        get a copy of the proxy

        :return: the copied proxy object
        :rtype: Proxy
        """
        p = object.__new__(type(self))
        p._roid = self._roid
        p._roMethods = self._roMethods
        p._roAttrs = self._roAttrs
        return p

    def __enter__(self):
        """
        For with control
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        For with control
        """
        # self.__del__()
        pass

    def __eq__(self, other):
        """
        == operator overload
        """
        if other is self:
            return True
        return isinstance(other, Proxy) and other._roid == self._roid

    def __ne__(self, other):
        """
        != operator overload
        """
        if other and isinstance(other, Proxy):
            return other._roid != self._roid
        return True

    def __hash__(self):
        """
        make proxy object hashable
        """
        return hash(self._roid)

    def __dir__(self):
        """
        support directory view for remote class
        """
        result = dir(self.__class__) + list(self.__dict__.keys())
        return sorted(set(result) | self._roMethods | self._roAttrs)

    # When special methods are invoked via special syntax (e.g. obj[index] calls
    # obj.__getitem__(index)), the special methods are not looked up via __getattr__
    # for efficiency reasons; instead, their presence is checked directly.
    # Thus we need to define them here to force (remote) lookup through __getitem__.
    def __bool__(self):
        """
        bool overload
        """
        return True

    def __len__(self):
        """
        define the len method to be same as remote
        """
        return self.__getattr__("__len__")()

    def __getitem__(self, index):
        """
        [] operator overload
        """
        return self.__getattr__("__getitem__")(index)

    def __setitem__(self, index, val):
        """
        []= operator overload
        """
        return self.__getattr__("__setitem__")(index, val)

    def __delitem__(self, index):
        """
        key delete overload
        """
        return self.__getattr__("__delitem__")(index)

    def __iter__(self):
        """
        iterator, to be implemented
        """
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
        """
        remote object method invoke

        :param methodname: remote method name
        :type methodname: str
        :param vargs: arg vector
        :type vargs: tuple
        :param kwargs: key word args
        :type kwargs: dict
        :return: method result
        :rtype: Any
        """
        msg_type = 3
        msg = {}
        vargs, kwargs = self._client._process_args(vargs, kwargs)
        msg["object_id"] = self._roid
        msg["method_name"] = methodname
        msg["vargs"] = vargs
        msg["kwargs"] = kwargs

        return self._client._send_msg(msg, msg_type)

    def _roGetMetadata(self):
        """
        Get remote class metadata

        :return: None
        :rtype: None
        """
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
        """
        Process remote class metadata

        :param metadata: remote class metadata
        :type metadata: Any
        :raises ZeroException: remote class does not allow its attributes to be revealed
        """
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
    def __init__(self, send, name):
        """
        method call abstraction

        :param send: send method
        :type send: callable
        :param name: method name
        :type name: str
        """
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        """
        get attribute for remote method, will return the method call
        """
        return _RemoteMethod(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args, **kwargs):
        """
        () operator overload
        intrigue the remote method call
        """
        return self.__send(self.__name, args, kwargs)
