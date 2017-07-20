"""
Message processor from spark bot
"""
import sys
import re
import time
from socket_server import ServerThread
from gerrit_msg.gerrit_processor import GerritProcessor
from jenkins_msg.jenkins_processor import JenkinsProcessor
import os.path


class MessageProcessor(object):
    def __init__(self, host, port, use_ssl=False):
        self.jenkins_processor = JenkinsProcessor()
        self.gerrit_processor = GerritProcessor()
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        if self.use_ssl:
            ssl_cert = "ssl_cert/ssl_cert"
            ssl_cert_key = "ssl_cert/ssl_cert_key"
            assert os.path.isfile(ssl_cert)
            assert os.path.isfile(ssl_cert_key)
            kwargs = {
                'certfile': ssl_cert,
                'keyfile': ssl_cert_key
            }
        else:
            kwargs = {}
        self.server = ServerThread(self.host, self.port, **kwargs)

    def start_server(self):
        self.server.start()

    def process(self, msg):
        print("Processing [{}]".format(msg.encode('utf-8')))
        if re.search(r'jenkins', msg, flags=re.I):
            resp = self.jenkins_processor.process(msg)
            return resp
        if re.search(r'gerrit', msg, flags=re.I):
            resp = self.gerrit_processor.process(msg)
            return resp
        else:
            return None

if __name__ == "__main__":
    mp = MessageProcessor("", 5559)
    msg = sys.argv[1]
    print(mp.process(msg))

