import threading
import socket
import ssl


def test_host(host, port):
    try:
        ip_addr = socket.gethostbyname(host)
        print("IP = {} port = {}".format(ip_addr, port))
    except socket.gaierror:
        print("Host name could not be resolved")
    return ip_addr


def create_socket():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
    except socket.error as msg:
        print('Failed to create socket Error code: ', str(msg))
    return s


def ssl_wrap(client, **kwargs):
    if kwargs:
        # print("SSL wrap", kwargs)
        client = ssl.wrap_socket(client, **kwargs)
        print("SSL wrap succeeded")
        return client
    else:
        print("SSL not used")
        return client


class TCPBase(threading.Thread):
    def __init__(self, host, port):
        self.s = create_socket()
        super(TCPBase, self).__init__()
        self.host = host
        self.port = port


            

