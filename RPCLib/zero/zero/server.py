# -------------------------------------------------------------------------------
# Engineering
# server.py
# -------------------------------------------------------------------------------
"""RPC server side module"""
# -------------------------------------------------------------------------------
# modified from https://github.com/Ananto30/zero under MIT license
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import asyncio
import inspect
import json
import logging
import os
import signal
import sys
import time
import typing
import uuid
import threading
from functools import partial
from importlib import import_module
from multiprocessing import Manager
from multiprocessing.pool import Pool

#import matplotlib
import msgpack

# import uvloop
import pandas as pd
import zmq
import zmq.asyncio

from zero.codegen import CodeGen
from zero.common import get_next_available_port

# Change
from zero.customtypes import ProxyObject, SecretObject
from zero.logger import _AsyncLogger
from zero.serialize import deserializer_table, serializer_table
from zero.type_util import (
    get_function_input_class,
    get_function_return_class,
    verify_allowed_type,
    verify_function_args,
    verify_function_input_type,
    verify_function_return,
)
from zero.zero_mq import ZeroMQ

logging.basicConfig(
    format="%(asctime)s  %(levelname)s  %(process)d  %(module)s > %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


def load_module(module: str):
    """
    load module into RPC server environment

    :param module: import module name
    :type module: str
    :return: a dictionary containing the classes and functions find in module
    :rtype: dict
    """
    m = import_module(module)
    safe_func_tuples = inspect.getmembers(m, inspect.isfunction)
    safe_object_tuples = inspect.getmembers(m, inspect.isclass)
    module_content = {}
    module_content["safe_funcs"] = set()
    module_content["safe_objects"] = set()
    for item in safe_func_tuples:
        if not item[0].startswith("_"):
            module_content["safe_funcs"].add(item[1])
    for item in safe_object_tuples:
        if not item[0].startswith("_"):
            module_content["safe_objects"].add(item[1])
    return module_content


def load_safe_function(name_module:str, name_class:str) -> None:
    module = import_module(name_module)
    list_function_tuple = inspect.getmembers(module, inspect.isclass)
    for function_tuple in list_function_tuple:
        object_class = function_tuple[1]
        return {name_class:object_class}

class Audit_log_task(threading.Thread):
    """
    Auxillary class for audit log server in isolated thread
    """
    def run(self):
        """
        Start async logger server
        """
        _AsyncLogger.start_log_poller(_AsyncLogger.ipc, _AsyncLogger.port)

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

        self._deserializer_table = deserializer_table
        self._serializer_table = serializer_table
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

        # verify_function_args(func)
        # verify_function_input_type(func)
        # verify_function_return(func)
        
        self._rpc_router[module_name] = func
        self._rpc_input_type_map[module_name] = get_function_input_class(func)
        self._rpc_return_type_map[module_name] = get_function_return_class(func)

    def register_ro(self, obj: object, module_name: str) -> None:
        """
        register remote object in rpc server

        :param obj: python object to be registered, should be python class
        :type obj: Any
        :param module_name: python moduled name where the obj comes from
        :type module_name: str
        :raises Exception: Can not register remote object starts with "_" (private class)
        """

        if obj.__name__.startswith("_"):
            raise Exception(f"Cannot register remote object for: {type(obj)}")

        self._ro_router[obj.__name__] = obj

    def read_initialization_vector(self) -> tuple:
        """
        read initialization vecotr, obtain researcher_id, researcher_user_id and data_federation_id

        :return: a tuple contains the three attributes
        :rtype: tuple
        """

        file_path = "/app/InitializationVector.json"
        iv_json = {}
        with open(file_path, "r") as f:
            iv_json = json.load(f)
        return iv_json["researcher_id"], iv_json["researcher_user_id"], iv_json["data_federation_id"]

    def run(self):
        """
        start server run
        """
        try:
            # utilize all the cores
            self._research_id, self._research_user_id, self._data_federation_id = self.read_initialization_vector()

            cores = os.cpu_count()

            #matplotlib.use("Agg")

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
                self._research_id,
                self._research_user_id,
                self._data_federation_id,
                self._rpc_input_type_map,
                self._rpc_return_type_map,
                self._secret_result_cache,
                self._secret_lock,
                self._serializer_table,
                self._deserializer_table,
            )
            self._pool.map_async(spawn_worker, [1])

            self._start_logger()
            self._start_queue_device()
            
            # TODO: by default we start the device with processes, but we need support to run only router
            # asyncio.run(self._start_router())

        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            self._terminate_server()
        except Exception as e:
            print(e)
            self._terminate_server()

    def _sig_handler(self, signum):
        """
        handle interupt signals

        :param signum: signal number received
        :type signum: int
        """
        print(f"{signal.Signals(signum).name} signal called")
        self._terminate_server()

    def _terminate_server(self):
        """
        terminate server run
        """
        print("Terminating server")
        self._pool.terminate()
        self._pool.close()
        self._pool.join()
        try:
            os.remove(self._device_ipc)
        except Exception as ex:
            raise ex
        sys.exit()

    def _start_queue_device(self):
        ZeroMQ.queue_device(self._host, self._port, self._device_ipc, self._device_port)

    def _start_logger(self):
        t = Audit_log_task()
        t.start()

    async def _start_router(self):  # pragma: no cover
        """
        start an asynchronous server
        """
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
        """
        handle asynchronous function call

        :param rpc: remote method name
        :type rpc: string
        :param msg: remote method args
        :type msg: Any
        :return: remote method return
        :rtype: Any
        """
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
        researcher_id: str,
        researcher_user_id: str,
        data_federation_id: str,
        rpc_input_type_map: dict,
        rpc_return_type_map: dict,
        secret_result_cache: dict,
        _secret_lock,
        serializer_table,
        deserializer_table,
        worker_id: int,
    ):
        """
        spawn a worker handling incoming request

        :param rpc_router: remote call router
        :type rpc_router: dict
        :param ro_router: remote object router
        :type ro_router: dict
        :param ipc: ipc method
        :type ipc: str
        :param port: server port
        :type port: int
        :param serializer: serialization method
        :type serializer: str
        :param rpc_input_type_map: input type dict for remote calls
        :type rpc_input_type_map: dict
        :param rpc_return_type_map: return type dict for remote calls
        :type rpc_return_type_map: dict
        :param secret_result_cache: result cache for object can not be revealed to the user
        :type secret_result_cache: dict
        :param _secret_lock: lock controlling the access to secret result cache from different processes
        :type _secret_lock: Manager.Lock
        :param worker_id: worker id
        :type worker_id: int
        """
        time.sleep(0.2)
        worker = _Worker(
            rpc_router,
            ro_router,
            ipc,
            port,
            serializer,
            researcher_id,
            researcher_user_id,
            data_federation_id,
            rpc_input_type_map,
            rpc_return_type_map,
            secret_result_cache,
            _secret_lock,
            serializer_table,
            deserializer_table,
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
        researcher_id,
        researcher_user_id,
        data_federation_id,
        rpc_input_type_map,
        rpc_return_type_map,
        secret_result_cache,
        _secret_lock,
        serializer_table,
        deserializer_table,
    ):
        """
        Request handling worker for RPC server

        :param rpc_router: rpc router dict
        :type rpc_router: dict
        :param ro_router: remote object router dict
        :type ro_router: dict
        :param ipc: ipc method
        :type ipc: str
        :param port: server port number
        :type port: int
        :param serializer: serialization method
        :type serializer: str
        :param rpc_input_type_map: input parameter types
        :type rpc_input_type_map: dict
        :param rpc_return_type_map: return types
        :type rpc_return_type_map: dict
        :param secret_result_cache: dict storing secret objects
        :type secret_result_cache: dict
        :param _secret_lock: lock controlling the access to secret object cache
        :type _secret_lock: Manager.Lock
        """
        self._rpc_router = rpc_router
        self._ro_router = ro_router
        self._ipc = ipc
        self._port = port
        self._serializer = serializer
        self._researcher_id = researcher_id
        self._researcher_user_id = researcher_user_id
        self._data_federation_id = data_federation_id
        self._loop = asyncio.new_event_loop()
        # self._loop = uvloop.new_event_loop()
        self._rpc_input_type_map = rpc_input_type_map
        self._rpc_return_type_map = rpc_return_type_map
        self.codegen = CodeGen(self._rpc_router, self._rpc_input_type_map, self._rpc_return_type_map)
        self._secret_result_cache = secret_result_cache
        self._secret_lock = _secret_lock
        self._async_logger = _AsyncLogger()
        self._serializer_table = serializer_table
        self._deserializer_table = deserializer_table
        self._init_serializer()

    def _init_serializer(self):
        """
        Initialize the serializer
        msgpack is the default serializer
        """
        if self._serializer == "msgpack":
            self._encode = msgpack.packb
            self._decode = msgpack.unpackb

    async def start_async_dealer_worker(self, worker_id):  # pragma: no cover
        """
        Start asynchronous request handling worker

        :param worker_id: worker id
        :type worker_id: int
        """
        ctx = zmq.asyncio.Context()
        socket = ctx.socket(zmq.DEALER)

        if os.name == "posix":
            socket.connect(f"ipc://{self._ipc}")
        else:
            socket.connect(f"tcp://127.0.0.1:{self._port}")

        logging.info(f"Starting worker: {worker_id}")

        async def process_message():
            """
            asynchronous message processor
            """
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
        """
        Synchronous request handling worker

        :param worker_id: worker id
        :type worker_id: int
        """

        def process_message(msg_type, msg):
            """
            synchronous message processer

            :param msg_type: message type
            :type msg_type: int
            :param msg: message payload
            :type msg: Any
            :return: processed message
            :rtype: Any
            """
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
        """
        Response handler, does:
        1. Identify if the response contains secret object, if so store the secret object in cache
        2. Identify if there are any return object is not basic python type, which requires a convertion

        :param response: response to the orchestrator
        :type response: Any
        :return: processed response
        :rtype: Any
        """
        
        name_class = str(type(response)).split(".")[-1][:-2] #TODO this is a bit ugly but the idea of getting the table in here is sound

        if isinstance(response, tuple):
            tmp_list = list(response)
            for i in range(len(tmp_list)):
                tmp_list[i] = self._handle_response(tmp_list[i])
            return tuple(tmp_list)
        elif isinstance(response, SecretObject) or isinstance(response, ProxyObject):
            with self._secret_lock:
                self._secret_result_cache[response.guid] = response.content
            response = response.to_dict()
        elif isinstance(response, pd.Series) or isinstance(response, pd.DataFrame):
            response = serializer_table[str(type(response))](response)
        elif name_class in self._serializer_table:
            response = response.to_dict()
        
        # elif isinstance(response, torch.nn.Module):
        #     response = serializer_table[str(torch.nn.Module)](response)
        #name_class = str(type(response))
        
         #   response = response.to_di

        return response

    def _handle_secret_msg(self, msg):
        #TODO This function needs a lot of cleanup
        """
        Handle input parameter which is a secret object
        If there is one, retrieve the secret object from cache

        :param msg: input parameter
        :type msg: Any
        :return: Processed input parameters
        :rtype: Any
        """
        import json
        print("_handle_secret_msg", flush=True)
        print(json.dumps(msg, sort_keys=False, indent=4), flush=True)
        print("dump", flush=True)
        if msg["vargs"] is not None:
            msg["vargs"] = list(msg["vargs"])
            for i in range(len(msg["vargs"])): #TODO use enumerate
                if isinstance(msg["vargs"][i], dict) and "__type__" in msg["vargs"][i]:
                    name_class = msg["vargs"][i]["__type__"]
                    print("found, do deser vargs", flush=True)
                    print(name_class, flush=True)
                    msg["vargs"][i] = self._deserializer_table[name_class].from_dict(msg["vargs"][i])
                elif isinstance(msg["vargs"][i], dict) and "object" in msg["vargs"][i]:
                    with self._secret_lock:
                        msg["vargs"][i] = self._secret_result_cache[msg["vargs"][i]["id"]] #TODO here the secret result cache comes in this should be merged with the service reference
        elif msg["kwargs"] is not None:
            for k, v in msg["kwargs"]:
                
                if isinstance(v, dict) and "__type__" in v:
                    name_class = msg["vargs"][i]["__type__"]
                    print("found, do deser kwargs", flush=True)
                    print(name_class, flush=True)
                    msg["kwargs"][k] = self._deserializer_table[name_class].from_dict(msg["vargs"][i])
                elif isinstance(v, dict) and "object" in v:
                    with self._secret_lock:
                        msg["kwargs"][k] = self._secret_result_cache[msg["kwargs"][k]["id"]] #TODO here the secret result cache comes in this should be merged with the service reference

        return msg

    def _handle_msg(self, msg_type, msg):
        """
        Handle incoming message by different types

        :param msg_type: message type
        :type msg_type: int
        :param msg: message payload
        :type msg: Any
        :return: processed message
        :rtype: Any
        """
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
        """
        call rpc function by different argument numbers

        :param func: call function
        :type func: function
        :param msg: input parameters
        :type msg: Any
        :return: function result
        :rtype: Any
        """

        if msg["vargs"] is None and msg["kwargs"] is None:
            return func()
        elif msg["kwargs"] is None:
            return func(*msg["vargs"])
        else:
            return func(*msg["vargs"], **msg["kwargs"])

    def _handle_function(self, msg):
        """
        Handle function call request

        :param msg: incoming message
        :type msg: Any
        :return: function result
        :rtype: Any
        """
        audit_msg = f"[function call][Researcher ID: {self._researcher_id}][Researcher user ID: {self._researcher_user_id}][Data Federation ID: {self._data_federation_id}] func_name:{msg['function_name']}; args:{msg['vargs']}; kwargs:{msg['kwargs']}"
        self._async_logger.log(audit_msg)

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
        """
        Handle a class method call

        :param msg: incoming message
        :type msg: Any
        :return: return result
        :rtype: Any
        """
        object_id = msg["object_id"]
        method_name = msg["method_name"]

        audit_msg = f"[Method call][Researcher ID: {self._researcher_id}][Researcher user ID: {self._researcher_user_id}][Data Federation ID: {self._data_federation_id}] object_id:{object_id}; method_name:{method_name}; args:{msg['vargs']}; kwargs:{msg['kwargs']}"
        self._async_logger.log(audit_msg)

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
        """
        Handle a constructor call request

        :param msg: incoming message
        :type msg: Any
        :return: output message
        :rtype: Any
        """
        class_name = msg["class_name"]

        audit_msg = f"[constructor call][Researcher ID: {self._researcher_id}][Researcher user ID: {self._researcher_user_id}][Data Federation ID: {self._data_federation_id}] class_name:{class_name}; args:{msg['vargs']}; kwargs:{msg['kwargs']}"
        self._async_logger.log(audit_msg)

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
        """
        Handle destructor call request

        :param msg: incoming message
        :type msg: Any
        """
        object_id = msg["object_id"]

        audit_msg = f"[destructor call][Researcher ID: {self._researcher_id}][Researcher user ID: {self._researcher_user_id}][Data Federation ID: {self._data_federation_id}] object_id:{msg['object_id']}"
        self._async_logger.log(audit_msg)

        try:
            obj = self._secret_result_cache[object_id]
            obj.__del__()
        except Exception as e:
            logging.exception(e)
            raise

    def _handle_attribute(self, msg):
        """
        Handle class attribute call request

        :param msg: incoming message
        :type msg: Any
        :return: output message
        :rtype: Any
        """
        object_id = msg["object_id"]

        audit_msg = f"[attribute call][Researcher ID: {self._researcher_id}][Researcher user ID: {self.researcher_user_id}][Data Federation ID: {self._data_federation_id}] object_id:{object_id}"
        self._async_logger.log(audit_msg)

        try:
            obj = self._secret_result_cache[object_id]
            attributes = []
            methods = []
            # to do handle private methods
            for item in dir(obj):
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
        """
        handle asynchronous call request

        :param rpc: rpc method
        :type rpc: function
        :param msg: incoming message
        :type msg: Any
        :return: output result
        :rtype: Any
        """
        if rpc in self._rpc_router:
            try:
                return await self._rpc_router[rpc](msg)
            except Exception as e:
                logging.exception(e)
        else:
            logging.error(f"method `{rpc}` is not found!")
