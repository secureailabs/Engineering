import msgpack
import zmq
import zmq.asyncio

from zero.type_util import verify_allowed_type


class ZeroPublisher:
    def __init__(self, host: str, port: int, use_async: bool = True):
        """
        _summary_

        :param host: _description_
        :type host: str
        :param port: _description_
        :type port: int
        :param use_async: _description_, defaults to True
        :type use_async: bool, optional
        """
        self.__host = host
        self.__port = port
        self.__socket = None
        if use_async:
            self._init_async_socket()
        else:
            self._init_sync_socket()

    def _init_sync_socket(self):
        """
        _summary_
        """
        ctx = zmq.Context()
        self.__socket: zmq.Socket = ctx.socket(zmq.PUB)
        self._set_socket_opt()
        self.__socket.connect(f"tcp://{self.__host}:{self.__port}")

    def _init_async_socket(self):
        """
        _summary_
        """
        ctx = zmq.asyncio.Context()
        self.__socket: zmq.Socket = ctx.socket(zmq.PUB)
        self._set_socket_opt()
        self.__socket.connect(f"tcp://{self.__host}:{self.__port}")

    def _set_socket_opt(self):
        """
        _summary_
        """
        # self.__socket.setsockopt(zmq.RCVTIMEO, 2000)
        self.__socket.setsockopt(zmq.LINGER, 0)

    def publish(self, topic, msg):
        """
        _summary_

        :param topic: _description_
        :type topic: _type_
        :param msg: _description_
        :type msg: _type_
        """
        verify_allowed_type(msg)
        self.__socket.send_multipart([topic.encode(), msgpack.packb(msg)])

    async def publish_async(self, topic, msg):
        """
        _summary_

        :param topic: _description_
        :type topic: _type_
        :param msg: _description_
        :type msg: _type_
        """
        verify_allowed_type(msg)
        await self.__socket.send_multipart([topic.encode(), msgpack.packb(msg)])
