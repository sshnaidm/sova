import datetime
import fileinput
import gzip
import json
import os
import re
import time

from lxml import etree
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()  # noqa

import tripleoci.config as config
from tripleoci.config import log
from tripleoci.patches import Job
from tripleoci.utils import Web, in_days

# Jobs regexps
branch_re = re.compile(r"--release ([^ ]+)")
ts_re = re.compile(r"(201\d-[01]\d-[0123]\d [012]\d:\d\d):\d\d\.\d\d\d")
pipe_re = re.compile(r'  Pipeline: (.+)')
job_re = re.compile(r'(.*)-(\d+)$')
timest_re = re.compile('\d+ \w+ 20\d\d  \d\d:\d\d:\d\d')
time_re = re.compile('^(\d+:\d+:\d+)')
ansible_ts = re.compile('n(\w+ \d\d \w+ 20\d\d  \d\d:\d\d:\d\d)')
stat_re = re.compile(
    r'ok=\d+\s*changed=\d+\s*unreachable=(\d+)\s*failed=(\d+)')
RDOCI_URL = 'https://thirdparty.logs.rdoproject.org/'
MAIN_INDEX = 'index_downci.html'
JENKINS_URL = 'https://rhos-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'


class Periodic(object):
    """Periodic job object

        Class that actually parses periodic jobs HTML page.
        It tries to extract all available info from the page, but
        some info could be found only in console.html, for example
        job status. So it needs to download console.html for every job and
        to parse it also.
    """
    def __init__(self, url=RDOCI_URL,
                 down_path=config.DOWNLOAD_PATH, limit=None):
        self.per_url = url
        self.down_path = down_path
        self.limit = limit
        self.jobs = self.get_jobs()

    def _get_index(self):
        path = os.path.join(self.down_path, MAIN_INDEX)
        if os.path.exists(path) and int(
                time.time() - os.stat(path).st_ctime
        ) < config.PLUGIN_RDOCI_CONFIG.main_index_timeout:
            with open(path) as f:
                index = f.read()
        else:
            req = None
            for t in range(10):
                web = Web(self.per_url, timeout=60)
                req = web.get()
                if req is None or int(req.status_code) != 200:
                    log.warning(
                        "Trying again to download rdo ci logs page ".format(
                            self.per_url))
                    time.sleep(30)
                else:
                    break
            if req is None or int(req.status_code) != 200:
                log.error(
                    "Can not retrieve rdo ci logs page {}".format(
                        self.per_url))
                return None
            with open(path, "wb") as f:
                f.write(req.content)
            index = req.content
        return index

    def _get_jenkins_json(self, job):
        path = os.path.join(
            self.down_path, job["log_hash"], "json.gz")
        if os.path.exists(path):
            log.debug("JSON is already here: {}".format(path))
            with gzip.open(path, "rt") as f:
                result = json.loads(f.read())
            return result
        elif os.path.exists(path + "_404"):
            return None
        json_url = os.path.join(
            JENKINS_URL,
            'job',
            job['name'],
            job['build_number'],
            'api', 'json')
        js_www = Web(url=json_url)
        js_web = js_www.get(ignore404=False)
        if js_web and js_web.ok:
            try:
                json_data = js_web.json()
            except Exception as e:
                log.warn("Can't parse JSON from {} - {}".format(
                    json_url, str(e)))
                return None
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with gzip.open(path, "wt") as f:
                f.write(json.dumps(json_data))
            return json_data
        elif js_web and js_web.status_code == 404:
            open(path + "_404", "a").close()
        return None

    def _get_logs_console(self, job, jenkins_console=False):
        console_names = config.ACTIVE_PLUGIN_CONFIG.console_name
        if not isinstance(console_names, list):
            console_names = [console_names]
        for console_name in console_names:
            path = os.path.join(
                self.down_path, job["log_hash"], console_name)
            if os.path.exists(path):
                log.debug("Console is already here: {}".format(path))
                return path
            if jenkins_console:
                console_url = os.path.join(
                    'https://ci.centos.org/job',
                    job['name'],
                    job['build_number'],
                    'timestamps/?time=yyyy-MM-dd%20HH:mm:ss&appendLog&locale=en_GB')
            else:
                console_url = job["log_url"] + "/" + console_name
            web = Web(console_url, timeout=7)
            log.debug("Trying to download console: {}".format(console_url))
            req = web.get(ignore404=True)
            if req is None or int(req.status_code) != 200:
                log.error("Failed to retrieve console: {}".format(console_url))
            else:
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                with gzip.open(path, "wb") as f:
                    f.write(req.content)
                break
        else:
            return None
        return path

    def parse_index(self, text):
        jobs = []
        et = etree.HTML(text)
        trs = [i for i in et.xpath("//tr") if not i.xpath("th")][1:]
        for tr in trs:
            td2 = tr.xpath("td")[1]
            link = td2.xpath("a")[0].attrib['href'].rstrip("/")
            if job_re.match(link):
                log_name, build = job_re.search(link).groups()
                job_name = log_name.replace('jenkins-', '')
                if job_name in config.TRACKED_JOBS:
                    job = {}
                    job["log_hash"] = job_name + "-" + build
                    job["log_url"] = RDOCI_URL + "/" + link + "/"
                    job["ts"] = datetime.datetime.strptime(
                        tr.xpath("td")[2].text.strip(),
                        "%Y-%m-%d %H:%M")
                    job["name"] = job_name
                    job['build_number'] = build
                    jobs.append(job)
        return sorted(jobs, key=lambda x: x['ts'], reverse=True)

    def _parse_ts(self, ts):
        return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M")

    def _get_more_data(self, j):
        def delta(e, s):
            return (self._parse_ts(e) - self._parse_ts(s)).seconds / 60

        start = end = last = None
        j.update({
            'status': 'UNKNOWN',
            'fail': True,
            'branch': '',
            'length': 0,
        })
        console = self._get_logs_console(job=j)
        if not console:
            log.error("Failed to get console for job {}".format(repr(j)))
            return None
        else:
            finput = fileinput.FileInput(console,
                                         openhook=fileinput.hook_compressed)
            for line in finput:
                line = line.decode()
                if ("Finished: SUCCESS" in line or
                        '[Zuul] Job complete, result: SUCCESS' in line):
                    j['fail'] = False
                    j['status'] = 'SUCCESS'
                elif ("Finished: FAILURE" in line or
                      "[Zuul] Job complete, result: FAILURE" in line or
                      "Build step 'Execute shell' marked build as failure"
                      in line):
                    j['fail'] = True
                    j['status'] = 'FAILURE'
                elif ("Finished: ABORTED" in line or
                        '[Zuul] Job complete, result: ABORTED' in line):
                    j['fail'] = True
                    j['status'] = 'ABORTED'
                if '  Pipeline:' in line:
                    j['pipeline'] = (pipe_re.search(line).group(1)
                                     if pipe_re.search(line) else '')
                if branch_re.search(line):
                    j['branch'] = branch_re.search(line).group(1)
                if ('Started by user' in line or
                        '[Zuul] Launched by' in line or
                        'Triggered by Gerrit' in line or
                        'Started by upstream' in line) and ts_re.search(line):
                    start = ts_re.search(line).group(1)
                if (("Finished: " in line or
                        '[Zuul] Job complete' in line or
                        'Performing Post build task' in line)
                        and ts_re.search(line)):
                    end = ts_re.search(line).group(1)
                if ts_re.search(line):
                    last = ts_re.search(line).group(1)
            end = end or last
            j['length'] = delta(end, start) if start and end else 0
            j['ts'] = self._parse_ts(end) if end else j['ts']
            finput.close()
            if not j.get('branch'):
                j['branch'] = 'master'
            if j['status'] == "UNKNOWN":
                json_data = self._get_jenkins_json(j)
                if json_data:
                    j['length'] = int(int(json_data["duration"]) / 1000)
                    if json_data["result"] != "SUCCESS":
                        j['status'] = 'FAILURE'
                        j['fail'] = True
                    else:
                        j['status'] = 'SUCCESS'
                        j['fail'] = False
                else:
                    j['status'] = 'FAILURE'
                    j['fail'] = True

        return j

    def get_jobs(self):
        index = self._get_index()
        if index:
            jobs = self.parse_index(index)[:self.limit]
        else:
            jobs = []
        jobs = [i for i in jobs if in_days(i, config.GATE_DAYS)]
        p = Pool(20)
        results = []
        for k, j in enumerate(jobs):
            results.append(p.spawn(self._get_more_data, j))
        p.join()
        for raw in [i.get() for i in results]:
            if raw is None:
                log.error("Failed to process job {}".format(repr(j)))
            else:
                yield PeriodicJob(**raw)


class PeriodicJob(Job):
    """Class that contains all necessary info for periodic job."""
    def __init__(self, **kwargs):
        super(PeriodicJob, self).__init__(
            name=kwargs["name"],
            log_url=kwargs["log_url"],
            status=kwargs["status"],
            length=kwargs["length"],
            timestamp=kwargs["ts"],
            pipeline=kwargs.get('pipeline') or '',
            patch=None,
            patchset=None
        )
        self.periodic = True
        self.branch = kwargs['branch']
