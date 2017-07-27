import datetime
import fileinput
import gzip
import os
import re
import time

from lxml import etree

import tripleoci.config as config
from tripleoci.config import log
from tripleoci.patches import Job
from tripleoci.utils import Web

# Jobs regexps
branch_re = re.compile(r"--release ([^ ]+)")
ts_re = re.compile(r"(201\d-[01]\d-[0123]\d [012]\d:\d\d):\d\d\.\d\d\d")
job_re = re.compile(r'(.*)-(\d+)$')
timest_re = re.compile('\d+ \w+ 20\d\d  \d\d:\d\d:\d\d')
time_re = re.compile('^(\d+:\d+:\d+)')
ansible_ts = re.compile('n(\w+ \d\d \w+ 20\d\d  \d\d:\d\d:\d\d)')
stat_re = re.compile(r'ok=\d+\s*changed=\d+\s*unreachable=(\d+)\s*failed=(\d+)')

RDOCI_URL = 'https://ci.centos.org/artifacts/rdo/'

MAIN_INDEX = 'index_rdoci.html'

class RDO_CI(object):
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
                        time.time() - os.stat(path).st_ctime) < 86400:
            with open(path) as f:
                index = f.read()
        else:
            web = Web(self.per_url, timeout=20)
            req = web.get()
            if req is None or int(req.status_code) != 200:
                log.warning(
                    "Trying again to download rdo ci logs page ".format(
                        self.per_url))
                req = web.get()
                if req is None or int(req.status_code) != 200:
                    log.error(
                        "Can not retrieve rdo ci logs page {}".format(
                            self.per_url))
                    return None
            with open(path, "wb") as f:
                f.write(req.content)
            index = req.content
        return index

    def _get_console(self, job):
        path = os.path.join(
            self.down_path, job["log_hash"], "console.html.gz")
        if os.path.exists(path):
            log.debug("Console is already here: {}".format(path))
            return path
        console_url = os.path.join(
            'https://ci.centos.org/job',
            job['name'],
            job['build_number'],
            'timestamps/?time=HH:mm:ss&appendLog&locale=en_GB')

        web = Web(console_url)
        req = web.get(ignore404=True)
        if req is not None and int(req.status_code) == 404:
            #url = job["log_url"] + "/console.txt"
            web = Web(url=console_url)
            log.debug("Trying to download raw console")
            req = web.get()
        if req is None or int(req.status_code) != 200:
            log.error("Failed to retrieve console: {}".format(job["log_url"]))
            return self._get_logs_console(job, path)
        else:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with gzip.open(path, "wb") as f:
                f.write(req.content)
        return path


    def _get_logs_console(self, job, path):
        web = Web(job['log_url'] + "/console.txt.gz")
        req = web.get(ignore404=True)
        if not req.ok:
            return None
        else:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with gzip.open(path, "wb") as f:
                f.write(req.content)
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
                if job_name in config.RDOCI_JOBS:
                    job = {}
                    job["log_hash"] = job_name + "-" + build
                    job["log_url"] = RDOCI_URL + "/" + link + "/"
                    job["ts"] = datetime.datetime.strptime(
                        tr.xpath("td")[2].text.strip(),
                        "%Y-%m-%d %H:%M")
                    job["name"] = job_name
                    job['build_number'] = build
                    jobs.append(job)
        print(sorted(jobs, key=lambda x: x['ts'], reverse=True))
        return sorted(jobs, key=lambda x: x['ts'], reverse=True)

    def _parse_ts(self, ts):
        return datetime.datetime.strptime(ts, '%H:%M:%S')

    def _parse_ts_orig(self, ts):
        return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M")

    def _get_more_data(self, j):
        def delta(e, s):
            return int((self._parse_ts(e) - self._parse_ts(s)).seconds / 60)

        def delta_orig(e, s):
            return int((self._parse_ts_orig(e) -
                        self._parse_ts_orig(s)).seconds / 60)

        def delta_ts(e, s):
            return int((e - s).seconds / 60)

        def _detect_branch(s):
            for br in config.GERRIT_BRANCHES:
                if "/" in br:
                    br_str = br.split("/")[1]
                else:
                    br_str = br
                if br_str in s:
                    return br

        start = end = None
        j.update({
            'status': 'FAILURE',
            'fail': True,
            'branch': '',
            'length': 0,
        })
        console = self._get_console(j)
        if not console:
            log.error("Failed to get console for periodic {}".format(repr(j)))
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
                        '[Zuul] Job complete, result: FAILURE' in line):
                    j['fail'] = True
                    j['status'] = 'FAILURE'
                elif ("Finished: ABORTED" in line or
                        '[Zuul] Job complete, result: ABORTED' in line):
                    j['fail'] = True
                    j['status'] = 'ABORTED'
                if branch_re.search(line):
                    branch = _detect_branch(branch_re.search(line).group(1))
                    if branch:
                        j['branch'] = branch
                try:
                    if start is None and time_re.search(line):
                        start = time_re.search(line).group(1)
                    if timest_re.search(line):
                        end = time_re.search(line).group(1)
                except Exception as e:
                    pass
            j['length'] = delta(end, start) if start and end else 0
            #j['ts'] = self._parse_ts(end) if end else j['ts']
            finput.close()
            if not j.get('branch'):
                j['branch'] = 'master'
            if j['length'] == 0:
                with gzip.open(console) as f:
                    text = str(f.read())
                ans_ts = ansible_ts.findall(text)
                start = datetime.datetime.strptime(ans_ts[0],
                                                   '%A %d %B %Y %H:%M:%S')
                j['length'] = delta_ts(j['ts'], start) + 300
                if list(set(stat_re.findall(text))) == [('0', '0')]:
                    j['status'] = 'SUCCESS'
                    j['fail'] = False
        return j

    def get_jobs(self):
        index = self._get_index()
        if index:
            jobs = self.parse_index(index)[:self.limit]
        else:
            jobs = []
        for j in jobs:
            raw = self._get_more_data(j)
            if raw is None:
                log.error("Failed to process job {}".format(repr(j)))
            else:
                yield RDOCIJob(**raw)


class RDOCIJob(Job):
    """Class that contains all necessary info for periodic job."""
    def __init__(self, **kwargs):
        super(RDOCIJob, self).__init__(
            name=kwargs["name"],
            log_url=kwargs["log_url"],
            status=kwargs["status"],
            length=kwargs["length"],
            timestamp=kwargs["ts"],
            patch=None,
            patchset=None
        )
        self.periodic = False
        self.branch = kwargs['branch']
