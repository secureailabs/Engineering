import asyncio
import logging
import sys
import typing
from multiprocessing import Process

import msgpack
import zmq
import zmq.asyncio

logging.basicConfig(
    format="%(asctime)s | %(threadName)s | %(process)d | %(module)s : %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


class ZeroSubscriber:
    def __init__(self, host: str = "127.0.0.1", port: int = 5558):
        """
        _summary_

        :param host: _description_, defaults to "127.0.0.1"
        :type host: str, optional
        :param port: _description_, defaults to 5558
        :type port: int, optional
        """
        self.__topic_map = {}
        self.__host = host
        self.__port = port

    def register_listener(self, topic: str, func: typing.Callable):
        """
        _summary_

        :param topic: _description_
        :type topic: str
        :param func: _description_
        :type func: typing.Callable
        :raises Exception: _description_
        """
        if not isinstance(func, typing.Callable):
            raise Exception(f"topic should listen to function not {type(func)}")
        self.__topic_map[topic] = func

    def run(self):
        """
        _summary_
        """
        processes = []
        try:
            processes = [
                Process(
                    target=Listener.spawn_listener_worker,
                    args=(topic, self.__topic_map[topic]),
                )
                for topic in self.__topic_map
            ]
            [prcs.start() for prcs in processes]
            self._create_zmq_device()
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            [prcs.terminate() for prcs in processes]
        else:
            print("Normal termination")
            [prcs.close() for prcs in processes]
        [prcs.join() for prcs in processes]

    def _create_zmq_device(self):
        """
        _summary_
        """
        try:
            ctx = zmq.Context()

            gateway = ctx.socket(zmq.SUB)
            gateway.bind(f"tcp://*:{self.__port}")
            gateway.setsockopt_string(zmq.SUBSCRIBE, "")

            logging.info(f"Starting server at {self.__port}")

            backend = ctx.socket(zmq.PUB)
            if sys.platform == "posix":
                backend.bind("ipc://backendworker")
            else:
                backend.bind("tcp://127.0.0.1:6667")

            zmq.device(zmq.FORWARDER, gateway, backend)

        except Exception as e:
            logging.error(e)
            logging.error("bringing down zmq device")
        finally:
            gateway.close()
            backend.close()
            ctx.term()


class Listener:
    @classmethod
    def spawn_listener_worker(cls, topic, func):
        """
        _summary_

        :param topic: _description_
        :type topic: _type_
        :param func: _description_
        :type func: _type_
        """
        worker = Listener(topic, func)
        asyncio.run(worker._create_worker())

    def __init__(self, topic, func):
        """
        _summary_

        :param topic: _description_
        :type topic: _type_
        :param func: _description_
        :type func: _type_
        """
        self.__topic = topic
        self.__func = func

    async def _create_worker(self):
        """
        _summary_
        """
        ctx = zmq.asyncio.Context()
        socket = ctx.socket(zmq.SUB)

        if sys.platform == "posix":
            socket.connect("ipc://backendworker")
        else:
            socket.connect("tcp://127.0.0.1:6667")

        socket.setsockopt_string(zmq.SUBSCRIBE, self.__topic)
        logging.info(f"Starting listener for: {self.__topic}")

        while True:
            topic, msg = await socket.recv_multipart()
            try:
                await self._handle_msg(msgpack.unpackb(msg))
            except Exception as e:
                logging.error(e)

    async def _handle_msg(self, msg):
        """
        _summary_

        :param msg: _description_
        :type msg: _type_
        :return: _description_
        :rtype: _type_
        """
        try:
            return await self.__func(msg)
        except Exception as e:
            logging.exception(e)
