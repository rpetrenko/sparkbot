from requests.auth import HTTPDigestAuth
from pygerrit.rest import GerritRestAPI
import os


class GerritProcessorException(Exception):
    def __init__(self, *args, **kwargs):
        super(GerritProcessorException, self).__init__(*args, **kwargs)


class GerritProcessor(object):
    def __init__(self):
        uri = os.environ.get("GERRIT_URL")
        username = os.environ.get("GERRIT_USER")
        password = os.environ.get("GERRIT_PASS")
        if not uri or not username or not password:
            err_msg = "Set environment variables GERRIT_URL, GERRIT_USER, GERRIT_PASS"
            print(err_msg)
            print("WARNING: gerrit commands will be ignored")
            self.rest = None
        else:
            self.auth = HTTPDigestAuth(username, password)
            self.rest = GerritRestAPI(url=uri, auth=self.auth)

    def process(self, msg):
        if not self.rest:
            return "gerrit commands ignored"
        supported = [
            'status open'
        ]
        if 'status open' in msg:
                gurl = ""
                # gurl = "q/status:open%20owner:self"
                print("URL:[{}]".format(gurl))
                changes = self.rest.get(gurl)
                return changes
        else:
            return "Supported gerrit messages {}".format(supported)
