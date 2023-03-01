class Session:
    def __init__(self, ip, port, use_ssl=False):
        self.ip = ip
        self.port = port
        self.use_ssl = use_ssl

    def get_url(self):
        if self.use_ssl:
            return f"https://{self.ip}:{self.port}"
        else:
            return f"http://{self.ip}:{self.port}"
