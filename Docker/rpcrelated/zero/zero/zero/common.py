def get_next_available_port(port):
    """
    _summary_

    :param port: _description_
    :type port: _type_
    :return: _description_
    :rtype: _type_
    """
    import socket
    from contextlib import closing

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        while sock.connect_ex(("127.0.0.1", port)) == 0:
            port += 1
        return port
