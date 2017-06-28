"""
Message processor from spark bot
"""
import sys
import re

from gerrit_msg.gerrit_processor import GerritProcessor
from jenkins_msg.jenkins_processor import JenkinsProcessor


class MessageProcessor(object):
    def __init__(self):
        self.jenkins_api = JenkinsProcessor()
        self.gerrit_api = GerritProcessor()

    def process(self, msg):
        print("Processing [{}]".format(msg.encode('utf-8')))
        if re.search(r'jenkins', msg, flags=re.I):
            resp = self.jenkins_api.process(msg)
            return resp
        if re.search(r'gerrit', msg, flags=re.I):
            resp = self.gerrit_api.process(msg)
            return resp
        else:
            return None

if __name__ == "__main__":
    mp = MessageProcessor()
    msg = sys.argv[1]
    print(mp.process(msg))

