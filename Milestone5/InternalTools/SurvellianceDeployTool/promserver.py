'''
Secure AI Labs
Jingwei Zhang
jingwei@secureailabs.com

A simple server running on prometheus server side to update
targets.json. When new VMs are spawn, the ips are going to
be added into the targets.json, such that the prometheus server
can automatically discover these new ips.
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import fcntl


class Server(BaseHTTPRequestHandler):
    '''
    base server class to handle post requests
    '''
    def _set_response(self):
        '''
        set response to 200, getting back to the clients
        '''
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        '''
        handle post request, extract ips and ports, and process them
        '''
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        request = json.loads(post_data)
        self.writeJson(request)
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def writeJson(self, data):
        '''
        add ips and ports into targets.json
        '''
        config = 0
        with open("./prometheus-2.32.1.linux-amd64/targets.json", 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            config = json.load(f)
            config[0]['targets'].append(data['ip']+":"+data['port'])
            json.dump(config, f)
            fcntl.flock(f, fcntl.LOCK_EX)


def run(server_class=HTTPServer, handler_class=Server, port=9999):
    '''
    run server on port 9999
    '''
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    run()
