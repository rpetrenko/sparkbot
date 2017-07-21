"""
Message processor from spark bot
"""
import re
import sys

from gerrit_msg.gerrit_processor import GerritProcessor
from jenkins_msg.jenkins_processor import JenkinsProcessor


class MessageProcessor(object):
    def __init__(self):
        self.jenkins_processor = JenkinsProcessor()
        self.gerrit_processor = GerritProcessor()

    def _process_by_subprocessor(self, msg):
        print("Processing [{}]".format(msg.encode('utf-8')))
        resp = ''
        if re.search(r'jenkins', msg, flags=re.I):
            resp = self.jenkins_processor.process(msg)
        elif re.search(r'gerrit', msg, flags=re.I):
            resp = self.gerrit_processor.process(msg)
        print("Response: {}".format(resp))
        return resp

    def _expand_keywords(self, msg):
        print("Expanding keywords")
        return msg

    def process(self, msg):
        msg = self._expand_keywords(msg)
        resp = self._process_by_subprocessor(msg)
        return resp


if __name__ == "__main__":
    mp = MessageProcessor()
    msg = sys.argv[1]
    print(mp.process(msg))

