"""
Message processor from spark bot
"""
import sys

from gerrit_msg.gerrit_processor import GerritProcessor
from jenkins_msg.jenkins_processor import JenkinsProcessor


class MessageProcessor(object):
    def __init__(self):
        self.jenkins_api = JenkinsProcessor()
        self.gerrit_api = GerritProcessor()

    def process(self, msg):
        print("Processing [{}]".format(msg))
        if 'jenkins' in msg:
            resp = self.jenkins_api.process(msg)
            return resp
        elif 'gerrit' in msg:
            self.gerrit_api.process(msg)
            return "using gerrit api"
        else:
            return None

if __name__ == "__main__":
    mp = MessageProcessor()
    msg = sys.argv[1]
    print(mp.process(msg))

