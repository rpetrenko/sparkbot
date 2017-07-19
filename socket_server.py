import time
import socket
import ssl
from common.common import TCPBase, test_host, create_socket, ssl_wrap


class ServerThread(TCPBase):
    def __init__(self, host, port, certfile=None, keyfile=None):
        super(ServerThread, self).__init__(host, port)
        self.s = create_socket()
        self.certfile = certfile
        self.keyfile = keyfile
        self.data = None
        self.response = None

    def binding(self):
        self.s.bind((self.host, self.port))
        print("Binding done")

    def listening(self):
        self.s.listen(10)

    def accept_connection(self):
        client, address = self.s.accept()
        print("Accepted client connection to address " + str(address))
        return client, address

    def run(self):
        self.binding()
        self.listening()
        while True:
            client, address = self.accept_connection()
            if self.certfile and self.keyfile:
                client = ssl_wrap(client,
                                  server_side=True,
                                  certfile=self.certfile,
                                  keyfile=self.keyfile)
            try:
                if self.data:
                    client.send(self.data)
                self.response = client.recv(1024)
                # data = client.recv(1024)
                # if data:
                #     print("server recv: {}".format(data))
                #     print("server send: Got {}".format(data))
                #     client.send("Got " + data)
            finally:
                client.close()
        self.s.close()
        print("exit server")
            

def main():
    host = ""
    port = 5558
    test_host(host, port)
    ssl_keyfile = "ssl_cert/ssl_cert_key"
    ssl_certfile = "ssl_cert/ssl_cert"

    server = ServerThread(host, port,
                          certfile=ssl_certfile, keyfile=ssl_keyfile)
    server.start()
    while server.isAlive():
        time.sleep(0.100)

if __name__ == "__main__":
    main()