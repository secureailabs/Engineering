# -------------------------------------------------------------------------------
# Engineering
# common.py
# -------------------------------------------------------------------------------
"""common tools for RPC module"""
# -------------------------------------------------------------------------------
# modified from https://github.com/Ananto30/zero under MIT license
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------


def get_next_available_port(port):
    """
    get next available port

    :param port: port number
    :type port: int
    :return: next port number
    :rtype: int
    """
    import socket
    from contextlib import closing

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        while sock.connect_ex(("127.0.0.1", port)) == 0:
            port += 1
        return port
