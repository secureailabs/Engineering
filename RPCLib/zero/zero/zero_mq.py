# -------------------------------------------------------------------------------
# Engineering
# zero_mq.py
# -------------------------------------------------------------------------------
"""Zero MQ multiprocess worker module"""
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
import os
from typing import Callable

import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

"""
If we want to replace the client-server patter with other implementation like Simple Pirate pattern,
implement the ZeroMQInterface class and replace the ZeroMQ with the new implementation instance.
"""



class ZeroMQInterface:
    def queue_device(
        self,
        worker_ipc: str,
        worker_port: int,
        host: str,
        port: int,
    ):
        """
        A queue_device maintains a queue to distribute the requests among the workers.

        Remember the queue device is blocking.

        Parameters
        ----------
        worker_ipc: str
            The address where all worker will connect.
            By default we use ipc for faster communication.
            But some os don't support ipc, in that case we use tcp and need the worker_port.
        worker_port: int
            It is used if ipc is not supported by os.
        host: str
            The host address where the device will listen from clients.
        port: int
            The port where the device will listen from clients.
        """
        raise NotImplementedError()

    def worker(
        self,
        worker_ipc: str,
        worker_port: int,
        worker_id: int,
        process_message: Callable,
    ):
        """
        A worker is a process that will handle the requests.

        Parameters
        ----------
        worker_ipc: str
            The address where all worker will connect.
            By default we use ipc for faster communication.
            But some os don't support ipc, in that case we use tcp and need the worker_port.
        worker_port: int
            It is used if ipc is not supported by os.
        worker_id: int
            The id of the worker.
        process_message: Callable
            The function that will process the message.
            It takes the rpc method name and msg in parameters as bytes and should return the reply in bytes.

            def process_message(rpc: bytes, msg: bytes) -> bytes:
                ...
        """
        raise NotImplementedError()


class ZeroMQPythonDevice(ZeroMQInterface):
    def queue_device(
        self,
        host: str,
        port: int,
        worker_ipc: str,
        worker_port: int,
    ):
        """
        zero mq device for socket connection

        :param host: host ip
        :type host: str
        :param port: host port
        :type port: int
        :param worker_ipc: host worker ipc method
        :type worker_ipc: str
        :param worker_port: host worker port
        :type worker_port: int
        """

        path_dir_public_key_zero_mq = os.environ.get("PATH_DIR_PUBLIC_KEY_ZEROMQ")
        if path_dir_public_key_zero_mq is None:
            raise ValueError("environment variable not set: PATH_DIR_PUBLIC_KEY_ZEROMQ")
        if not os.path.isdir(path_dir_public_key_zero_mq):
            raise Exception(f"dir not found: {path_dir_public_key_zero_mq}")

        path_file_private_key_zero_mq_server = os.environ.get("PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER")
        if path_file_private_key_zero_mq_server is None:
            raise ValueError("environment variable not set: PATH_FILE_PRIVATE_KEY_ZEROMQ_SERVER")


        try:
            ctx = zmq.Context.instance()
            gateway = ctx.socket(zmq.ROUTER)

            auth = ThreadAuthenticator(ctx)
            auth.start()
            auth.configure_curve(domain="*", location=path_dir_public_key_zero_mq)

            server_public, server_secret = zmq.auth.load_certificate(path_file_private_key_zero_mq_server)
            gateway.curve_secretkey = server_secret
            gateway.curve_publickey = server_public
            gateway.curve_server = True

            gateway.bind(f"tcp://{host}:{port}")
            logging.info(f"Starting server at {host}:{port}")

            backend = ctx.socket(zmq.DEALER)

            if os.name == "posix":
                backend.bind(f"ipc://{worker_ipc}")
            else:
                backend.bind(f"tcp://127.0.0.1:{worker_port}")

            zmq.device(zmq.QUEUE, gateway, backend)
            # zmq.proxy(gateway, backend, None)

            gateway.close()
            backend.close()
            auth.stop()
            ctx.term()
        except Exception as e:
            logging.exception(e)
            logging.error("bringing down zmq device")

    def worker(
        self,
        worker_ipc: str,
        worker_port: int,
        worker_id: int,
        process_message: Callable,
    ):
        """
        client worker

        :param worker_ipc: worker ipc method
        :type worker_ipc: str
        :param worker_port: worker port
        :type worker_port: int
        :param worker_id: worker id
        :type worker_id: int
        :param process_message: worked process function
        :type process_message: Callable
        """
        try:
            ctx = zmq.Context()
            socket = ctx.socket(zmq.DEALER)

            if os.name == "posix":
                socket.connect(f"ipc://{worker_ipc}")
            else:
                socket.connect(f"tcp://127.0.0.1:{worker_port}")

            logging.info(f"Starting worker: {worker_id}")

            while True:
                ident, rpc, msg = socket.recv_multipart()
                response = process_message(rpc, msg)
                socket.send_multipart([ident, response], zmq.DONTWAIT)

        except Exception as e:
            logging.exception(e)


# IMPORTANT: register the imlementation here
ZeroMQ = ZeroMQPythonDevice()
