import asyncio
import inspect
import logging
import os
import signal
import sys
import time
import typing
import uuid
import inspect
from functools import partial
from multiprocessing.pool import Pool
from multiprocessing import Manager

import matplotlib

import msgpack
import zmq
import zmq.asyncio

from .codegen import CodeGen
from .common import get_next_available_port
from .type_util import (
    get_function_input_class,
    get_function_return_class,
    verify_allowed_type,
    verify_function_args,
    verify_function_input_type,
    verify_function_return,
)
from .zero_mq import ZeroMQ

# Change
from .customtypes import SecretObject, ProxyObject

# import uvloop


logging.basicConfig(
    format="%(asctime)s  %(levelname)s  %(process)d  %(module)s > %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


def load_module(module):
    m = __import__(module)
    safe_func_tuples = inspect.getmembers(m, inspect.isfunction)
    safe_object_tuples = inspect.getmembers(m, inspect.isclass)
    module_content = {}
    module_content["safe_funcs"] = set()
    module_content["safe_objects"] = set()
    for item in safe_func_tuples:
        if not inspect.getmodule(item[1]) == m:
            continue
        if not item[0].startswith("_"):
            module_content["safe_funcs"].add(item[1])
    for item in safe_object_tuples:
        if not inspect.getmodule(item[1]) == m:
            continue
        if not item[0].startswith("_"):
            module_content["safe_objects"].add(item[1])
    return module_content


class ZeroServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 5559):
        """
        ZeroServer registers rpc methods that are called from a ZeroClient.

        By default ZeroServer uses all of the cores for best performance possible.
        A zmq queue device load balances the requests and runs on the main thread.

        Ensure to run the server inside
        `if __name__ == "__main__":`
        As the server runs on multiple processes.

        Parameters
        ----------
        host: str
            Host of the ZeroServer.
        port: int
            Port of the ZeroServer.

        """
        self._port = port
        self._host = host
        self._serializer = "msgpack"
        self._rpc_router = {}
        self._ro_router = {}

        # Stores rpc functions `msg` types
        self._rpc_input_type_map = {}
        self._rpc_return_type_map = {}

        # Change
        self._manager = Manager()
        self._secret_result_cache = self._manager.dict()
        self._secret_lock = self._manager.Lock()
        # ------

    def register_rpc(self, func: typing.Callable, module_name):
        """
        Register the rpc methods available for clients.
        Make sure they return something.
        If the methods don't return anything, it will get timeout in client.

        Parameters
        ----------
        func: typing.Callable
            RPC function.
        """
        if not isinstance(func, typing.Callable):
            raise Exception(f"register function; not {type(func)}")
        if func.__name__ in self._rpc_router:
            raise Exception(f"Cannot have two RPC function same name: `{func.__name__}`")
        if func.__name__ == "get_rpc_contract":
            raise Exception("get_rpc_contract is a reserved function; cannot have `get_rpc_contract` as a RPC function")

        verify_function_args(func)
        verify_function_input_type(func)
        verify_function_return(func)

        self._rpc_router[module_name + "." + func.__name__] = func
        self._rpc_input_type_map[func.__name__] = get_function_input_class(func)
        self._rpc_return_type_map[func.__name__] = get_function_return_class(func)

    def register_ro(self, obj, module_name):

        if obj.__name__.startswith("_"):
            raise Exception(f"Cannot register remote object for: {type(obj)}")

        self._ro_router[module_name + "." + obj.__name__] = obj

    def run(self):
        try:
            # utilize all the cores
            cores = os.cpu_count()

            matplotlib.use("Agg")

            # device port is used for non-posix env
            self._device_port = get_next_available_port(6666)

            # ipc is used for posix env
            self._device_ipc = uuid.uuid4().hex[18:] + ".ipc"

            # this is important to catch KeyboardInterrupt
            original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

            self._pool = Pool(cores)

            signal.signal(signal.SIGINT, original_sigint_handler)  # for KeyboardInterrupt
            signal.signal(signal.SIGTERM, self._sig_handler)  # for process termination

            spawn_worker = partial(
                _Worker.spawn_worker,
                self._rpc_router,
                self._ro_router,
                self._device_ipc,
                self._device_port,
                self._serializer,
                self._rpc_input_type_map,
                self._rpc_return_type_map,
                self._secret_result_cache,
                self._secret_lock,
            )
            self._pool.map_async(spawn_worker, list(range(1, cores + 1)))

            self._start_queue_device()

            # TODO: by default we start the device with processes, but we need support to run only router
            # asyncio.run(self._start_router())

        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            self._terminate_server()
        except Exception as e:
            print(e)
            self._terminate_server()

    def _sig_handler(self, signum, frame):
        print(f"{signal.Signals(signum).name} signal called")
        self._terminate_server()

    def _terminate_server(self):
        print("Terminating server")
        self._pool.terminate()
        self._pool.close()
        self._pool.join()
        try:
            os.remove(self._device_ipc)
        except:
            pass
        sys.exit()

    def _start_queue_device(self):
        ZeroMQ.queue_device(self._host, self._port, self._device_ipc, self._device_port)

    async def _start_router(self):  # pragma: no cover
        ctx = zmq.asyncio.Context()
        socket = ctx.socket(zmq.ROUTER)
        socket.bind(f"tcp://127.0.0.1:{self._port}")
        logging.info(f"Starting server at {self._port}")

        while True:
            ident, rpc, msg = await socket.recv_multipart()
            rpc_method = rpc.decode()
            response = await self._handle_msg(rpc_method, msgpack.unpackb(msg))
            try:
                verify_allowed_type(response, rpc_method)
            except Exception as e:
                logging.exception(e)
            await socket.send_multipart([ident, msgpack.packb(response)])

    async def _handle_msg(self, rpc, msg):  # pragma: no cover
        if rpc in self._rpc_router:
            try:
                return await self._rpc_router[rpc](msg)
            except Exception as e:
                logging.exception(e)
        else:
            logging.error(f"{rpc} is not found!")


class _Worker:
    @classmethod
    def spawn_worker(
        cls,
        rpc_router: dict,
        ro_router: dict,
        ipc: str,
        port: int,
        serializer: str,
        rpc_input_type_map: dict,
        rpc_return_type_map: dict,
        secret_result_cache: dict,
        _secret_lock,
        worker_id: int,
    ):
        time.sleep(0.2)
        worker = _Worker(
            rpc_router,
            ro_router,
            ipc,
            port,
            serializer,
            rpc_input_type_map,
            rpc_return_type_map,
            secret_result_cache,
            _secret_lock,
        )
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(worker.create_worker(worker_id))
        # asyncio.run(worker.start_async_dealer_worker(worker_id))
        worker.start_dealer_worker(worker_id)

    def __init__(
        self,
        rpc_router,
        ro_router,
        ipc,
        port,
        serializer,
        rpc_input_type_map,
        rpc_return_type_map,
        secret_result_cache,
        _secret_lock,
    ):
        self._rpc_router = rpc_router
        self._ro_router = ro_router
        self._ipc = ipc
        self._port = port
        self._serializer = serializer
        self._loop = asyncio.new_event_loop()
        # self._loop = uvloop.new_event_loop()
        self._rpc_input_type_map = rpc_input_type_map
        self._rpc_return_type_map = rpc_return_type_map
        self.codegen = CodeGen(self._rpc_router, self._rpc_input_type_map, self._rpc_return_type_map)
        self._secret_result_cache = secret_result_cache
        self._secret_lock = _secret_lock
        self._init_serializer()

    def _init_serializer(self):
        # msgpack is the default serializer
        if self._serializer == "msgpack":
            self._encode = msgpack.packb
            self._decode = msgpack.unpackb

    async def start_async_dealer_worker(self, worker_id):  # pragma: no cover
        ctx = zmq.asyncio.Context()
        socket = ctx.socket(zmq.DEALER)

        if os.name == "posix":
            socket.connect(f"ipc://{self._ipc}")
        else:
            socket.connect(f"tcp://127.0.0.1:{self._port}")

        logging.info(f"Starting worker: {worker_id}")

        async def process_message():
            try:
                ident, rpc, msg = await socket.recv_multipart()
                rpc_method = rpc.decode()
                msg = self._decode(msg)
                response = await self._handle_msg_async(rpc_method, msg)
                response = self._encode(response)
                await socket.send_multipart([ident, response], zmq.DONTWAIT)
            except Exception as e:
                logging.exception(e)

        while True:
            await process_message()

    def start_dealer_worker(self, worker_id):
        def process_message(msg_type, msg):
            try:
                msg_type = self._decode(msg_type)
                msg = self._decode(msg, use_list=False, strict_map_key=False)
                response = self._handle_msg(msg_type, msg)
                response = self._handle_response(response)
                return self._encode(response)
            except Exception as e:
                print("-------------------Exception-------------------------")
                response = {
                    "object": 0,
                    "Message": "This error happen remotely:\n" + str(e) + "\n------------------------",
                }
                logging.exception(e)
                print("------------------------------------------------------")
                return self._encode(response)

        ZeroMQ.worker(self._ipc, self._port, worker_id, process_message)

    # Change
    def _handle_response(self, response):
        if isinstance(response, tuple):
            tmp_list = list(response)
            for i in range(len(tmp_list)):
                tmp_list[i] = self._handle_response(tmp_list[i])
            return tuple(tmp_list)
        elif isinstance(response, SecretObject) or isinstance(response, ProxyObject):
            with self._seret_lock:
                self._secret_result_cache[response.guid] = response.content
            response = response.to_dict()
        return response

    def _handle_secret_msg(self, msg):
        if msg["vargs"] is not None:
            msg["vargs"] = list(msg["vargs"])
            for i in range(len(msg["vargs"])):
                if isinstance(msg["vargs"][i], dict) and "object" in msg["vargs"][i]:
                    with self._secret_lock:
                        msg["vargs"][i] = self._secret_result_cache[msg["vargs"][i]["id"]]
        elif msg["kwargs"] is not None:
            for k, v in msg["kwargs"]:
                if isinstance(v, dict) and "object" in v:
                    with self._secret_lock:
                        msg["kwargs"][k] = self._secret_result_cache[msg["kwargs"][k]["id"]]
        return msg

    def _handle_msg(self, msg_type, msg):
        if msg_type == 0:
            return self._handle_function(msg)
        elif msg_type == 1:
            return self._handle_constructor(msg)
        elif msg_type == 2:
            return self._handle_attribute(msg)
        elif msg_type == 3:
            return self._handle_method(msg)
        elif msg_type == 4:
            self._handle_destructor(msg)
            return
        else:
            logging.error(f"msg type `{msg_type}` is not found!")
            return {"__zerror__msg_type_not_found": f"msg `{msg_type}` is not found!"}

    def _call_function(self, func, msg):
        if msg["vargs"] is None and msg["kwargs"] is None:
            return func()
        elif msg["kwargs"] is None:
            return func(*msg["vargs"])
        else:
            return func(*msg["vargs"], **msg["kwargs"])

    def _handle_function(self, msg):
        rpc = msg["function_name"]
        if rpc in self._rpc_router:
            func = self._rpc_router[rpc]
            try:
                # TODO: is this a bottleneck
                msg = self._handle_secret_msg(msg)
                return self._call_function(func, msg)
            except Exception as e:
                logging.exception(e)
                raise
        else:
            logging.error(f"method `{rpc}` is not found!")
            return {"__zerror__method_not_found": f"method `{rpc}` is not found!"}

    def _handle_method(self, msg):
        object_id = msg["object_id"]
        method_name = msg["method_name"]

        try:
            obj = self._secret_result_cache[object_id]
            msg = self._handle_secret_msg(msg)
            method = 0
            if hasattr(obj, "__getattr__"):
                method = obj.__getattr__(method_name)
            elif hasattr(obj, "__getattribute__"):
                method = obj.__getattribute__(method_name)
            return self._call_function(method, msg)
        except Exception as e:
            logging.exception(e)
            raise

    def _handle_constructor(self, msg):
        class_name = msg["class_name"]

        if class_name in self._ro_router:
            try:
                cla = self._ro_router[class_name]
                msg = self._handle_secret_msg(msg)
                obj = cla(*msg["vargs"], **msg["kwargs"])
                return SecretObject(obj)
            except Exception as e:
                logging.exception(e)
                raise
        else:
            logging.error(f"class `{class_name}` is not found!")
            return {"__zerror__class_not_found": f"class `{class_name}` is not found!"}

    def _handle_destructor(self, msg):
        object_id = msg["object_id"]

        try:
            obj = self._secret_result_cache[object_id]
            obj.__del__()
        except Exception as e:
            logging.exception(e)
            raise

    def _handle_attribute(self, msg):
        object_id = msg["object_id"]

        try:
            obj = self._secret_result_cache[object_id]
            attributes = []
            methods = []
            for item in dir(obj):
                if not item.startswith("_"):
                    if hasattr(obj, "__getattr__"):
                        attr = obj.__getattr__(item)
                    elif hasattr(obj, "__getattribute__"):
                        attr = obj.__getattribute__(item)
                    if inspect.ismethod(attr):
                        methods.append(item)
                    else:
                        attributes.append(item)
            return {"attributes": attributes, "methods": methods}
        except Exception as e:
            logging.exception(e)
            raise

    async def _handle_msg_async(self, rpc, msg):  # pragma: no cover
        if rpc in self._rpc_router:
            try:
                return await self._rpc_router[rpc](msg)
            except Exception as e:
                logging.exception(e)
        else:
            logging.error(f"method `{rpc}` is not found!")