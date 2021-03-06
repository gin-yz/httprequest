import json
import socket
import ssl
import os

class client_ssl(object):
    def __init__(self,port_num):
        path = os.getcwd().replace('/','\\')
        self.CA_FILE = path + "\\utils\\ca.crt"
        self.KEY_FILE = path + "\\utils\\server.key"
        self.CERT_FILE = path + "\\utils\\server.crt"
        self.port_num = port_num
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self.context.check_hostname = False
        self.context.load_cert_chain(certfile=self.CERT_FILE, keyfile=self.KEY_FILE)
        self.context.load_verify_locations(self.CA_FILE)
        self.context.verify_mode = ssl.CERT_REQUIRED
    def send_msg(self, data):

        with socket.socket() as sock:
            with self.context.wrap_socket(sock, server_side=False) as ssock:
                ssock.connect(('127.0.0.1', self.port_num))
                send_data = json.dumps(data)
                ssock.send(send_data.encode())
                json_msg = ssock.recv(1024)
                ssock.close()
                msg = json.loads(json_msg.decode())
                return msg['key']
