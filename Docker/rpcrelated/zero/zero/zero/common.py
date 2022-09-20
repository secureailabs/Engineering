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
