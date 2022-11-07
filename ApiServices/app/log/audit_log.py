# -------------------------------------------------------------------------------
# Engineering
# audit_log.py
# -------------------------------------------------------------------------------

# """Module to write audit logs"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
# This software contains proprietary information which shall not
# be reproduced or transferred to other documents and shall not
# be disclosed to others for any purpose without
# prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import logging
import os
import sys

import zmq.asyncio


class _AsyncLogger:  # pragma: no cover
    """
    audit log with zeromq ipc
    """

    port = 13456
    ipc = "zerologger"

    def __init__(self):
        """
        logger initialization
        """
        # pass
        self.init_push_logger()

    def init_push_logger(self):
        """
        init log pusher
        """
        ctx = zmq.asyncio.Context()
        self.log_pusher = ctx.socket(zmq.PUSH)
        if os.name == "posix":
            self.log_pusher.connect(f"ipc://{_AsyncLogger.ipc}")
        else:
            self.log_pusher.connect(f"tcp://127.0.0.1:{_AsyncLogger.port}")

    def log(self, msg):
        """
        send log string to pusher

        :param msg: log message
        :type msg: str
        """
        self.log_pusher.send_string(str(msg))

    @staticmethod
    def start_log_poller(ipc, port):
        """
        start log poller

        :param ipc: ipc method
        :type ipc: str
        :param port: port number
        :type port: int
        """
        _AsyncLogger.port = port
        _AsyncLogger.ipc = ipc

        logger = logging.getLogger()
        file_handler = logging.FileHandler("audit.log")
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        ctx = zmq.Context()
        log_listener = ctx.socket(zmq.PULL)

        if os.name == "posix":
            log_listener.bind(f"ipc://{_AsyncLogger.ipc}")
            logging.info(f"Async logger starting at ipc://{_AsyncLogger.ipc}")
        else:
            log_listener.bind(f"tcp://127.0.0.1:{_AsyncLogger.port}")
            logging.info(f"Async logger starting at tcp://127.0.0.1:{_AsyncLogger.port}")
        try:
            while True:
                log = log_listener.recv_string()
                print(log)
                logger.info(log)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating async logger")
        except Exception as e:
            print(e)
        finally:
            log_listener.close()
            sys.exit()


logger = _AsyncLogger()


async def log_message(
    msg: str,
):
    """
    Send log message to async server

    :param msg: audit log message
    :type msg: str
    """
    logger.log(msg)
