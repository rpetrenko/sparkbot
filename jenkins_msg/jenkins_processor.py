import jenkins
import os
import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class JenkinsProcessorException(Exception):
    def __init__(self, *args, **kwargs):
        super(JenkinsProcessorException, self).__init__(*args, **kwargs)


class JenkinsProcessor(object):
    def __init__(self):
        uri = os.environ.get("JENKINS_URL")
        username = os.environ.get("JENKINS_USER")
        password = os.environ.get("JENKINS_PASS")
        if not uri or not username or not password:
            err_msg = "Set environment variabls JENKINS_URL, JENKINS_USER, JENKINS_PASS"
            raise JenkinsProcessorException(err_msg)
        self.server = jenkins.Jenkins(uri, username=username, password=password)
        user = self.server.get_whoami()
        print("Hello %s" % user['fullName'])
        # version = self.server.get_version()
        # print('Jenkins %s' % version)

    def _convert_time_to_mins(self, t):
        # milli seconds to seconds
        t /= 1000.
        # seconds to mins
        t /= 60.
        return "{} min".format(int(t))

    def _result_to_str(self, r):
        if r:
            return "Running"
        else:
            return "Done"

    def _started_to_date(self, t):
        # milisec to sec
        t /= 1000.
        return (
            datetime.datetime.fromtimestamp(
                int(t)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

    def process(self, msg):
        supported = [
            'get job info'
        ]
        if 'get job info' in msg:
            builds = set()
            job_name = msg.split()[-1]
            job_info = self.server.get_job_info(job_name)
            last = job_info['lastBuild']['number']
            builds.add(last)
            good = job_info['lastSuccessfulBuild']['number']
            builds.add(good)
            bad = job_info['lastFailedBuild']['number']
            builds.add(bad)
            resp = []
            for b in sorted(builds, reverse=True):
                info = self.server.get_build_info(job_name, b)
                r = "{}: {} - {} - {} - {}".format(
                                        b,
                                        info['result'],
                                        self._result_to_str(info['building']),
                                        self._convert_time_to_mins(info['duration']),
                                        self._started_to_date(info['timestamp'])
                )
                resp.append(r)
            return resp
        else:
            return "Supported jenkins messages {}".format(supported)