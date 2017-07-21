import jenkins
import os
import re
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
        # to trigger builds remotely
        self.api_token = os.environ.get("JENKINS_API_TOKEN", None)
        if not uri or not username or not password:
            err_msg = "Set environment variabls JENKINS_URL, JENKINS_USER, JENKINS_PASS"
            print(err_msg)
            print("WARNING: jenkins commands will be ignored")
            self.server = None
        else:
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

    def get_job_list_regex(self, pattern, folder_depth=4):
        result = []
        jobs = self.server.get_all_jobs(folder_depth)
        for job in jobs:
            if re.search(pattern, job['name']):
                job_name = job['fullname']
                result.append(job_name)
        return result

    def process(self, msg):
        if not self.server:
            return "jenkins commands ignored"
        supported = [
            'list jobs',
            'show last failure',
            'show last lines',
            'trigger build',
            'get job info'
        ]
        if 'list jobs' in msg:
            job_regex = msg.split()[-1]
            job_info = self.get_job_list_regex(job_regex)
            return job_info

        if 'show last failure' in msg:
            job_name = msg.split()[-1]
            job_info = self.server.get_job_info(job_name)
            bad = job_info['lastFailedBuild']['number']
            output = self.server.get_build_console_output(job_name, bad)
            m = re.search(r'Exception:(.*)', output)
            if m:
                output = m.groups(0)
            return output

        if 'show last lines' in msg:
            job_name = msg.split()[-1]
            job_info = self.server.get_job_info(job_name)
            last = job_info['lastBuild']['number']
            output = self.server.get_build_console_output(job_name, last)
            last_10 = output.split('\n')[-10:]
            return "\n".join(last_10)

        if 'trigger build' in msg:
            job_name = msg.split()[-1]
            if not self.api_token:
                raise JenkinsProcessorException("Set JENKINS_API_TOKEN as environment variable")
            job_info = self.server.get_job_info(job_name)
            params = job_info['actions'][0]['parameterDefinitions']
            pars = {}
            for p in params:
                name, value = p['name'], p['defaultParameterValue']
                if value:
                    pars[name] = value['value']
            self.server.build_job(job_name, token=self.api_token, parameters=pars)
            return "triggered"

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
