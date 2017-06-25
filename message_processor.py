"""
Message processor from spark bot
"""
import sys

class MessageProcessor(object):
    def __init__(self):
        jenkins_api = None
        gerrit_api = None

    def process(self, msg):
        msg = msg.lower()
        print("Processing [{}]".format(msg))
        if 'jenkins' in msg:
            return "using jenkins api"
        elif 'gerrit' in msg:
            return "using gerrit api"
        else:
            return None

if __name__ == "__main__":
    mp = MessageProcessor()
    msg = sys.argv[1]
    mp.process(msg)

