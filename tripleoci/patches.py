import datetime
import gzip
import os
import re
import time
import tripleoci.config as config
from tripleoci.config import log
from tripleoci.utils import Web


JOB_RE = re.compile(r"(\S+) (http://logs.openstack.org/\S+) "
                    r": (FAILURE|SUCCESS) in ([hms \d]+)")
JOB_RE2 = re.compile(r"(\S+) (https://review.rdoproject.org/\S+) "
                     r": (FAILURE|SUCCESS) in ([hms \d]+)")
PATCH_RE = re.compile(r"Patch Set (\d+):")
TIME_RE = re.compile(r"((?P<hour>\d+)h)? *((?P<min>\d+)m)? *((?P<sec>\d+)s)?")
RDO_RE = re.compile(r'Logs have been uploaded and are available at:'
                    r'.*(https://logs.rdoproject.org/[^<>\s]+)', re.DOTALL)
PIPE_RE = re.compile(r"([^ \(\)]+) pipeline")


def utc_delta():
    ts = time.time()
    utc_offset = (datetime.datetime.fromtimestamp(ts) -
                  datetime.datetime.utcfromtimestamp(ts)).total_seconds()
    return datetime.timedelta(seconds=utc_offset)

UTC_OFFSET = utc_delta()


class Patch(object):
    """Patch pbject

        Class that creates Patch object from patch data from gerrit.
        It contains various info the could be useful for reports.
    """
    def __init__(self, data):
        self.data = data
        self.branch = data['branch']
        self.project = data['project']
        self.status = data['status']
        self.topic = data.get('topic', '')
        self.url = data['url']
        self.commitmsg = data['commitMessage']
        self.created = datetime.datetime.fromtimestamp(data['createdOn'])
        self.lastup = datetime.datetime.fromtimestamp(data['lastUpdated'])
        self.patch_number = data['number']
        self.gid = data['id']
        self.owner = data['owner']
        self.sets = [Patchset(i, data) for i in data['patchSets']]
        self.current = Patchset(data['currentPatchSet'], data)
        self.comments = data['comments']
        self.jobs = self.get_jobs()
        self.subject = data['subject']

    def _extract_job_from_comment(self, comment):
        def parse_time(x):
            timest = TIME_RE.search(x.strip())
            hour, minute, sec = (int(i) for i in (
                timest.groupdict()['hour'] or 0,
                timest.groupdict()['min'] or 0,
                timest.groupdict()['sec'] or 0))
            # Resolution in minutes
            return 60 * hour + minute

        def _get_jenkins_console(x):
            consoles_dir = os.path.join(config.DOWNLOAD_PATH, "jenkins_cons")
            if not os.path.exists(consoles_dir):
                os.makedirs(consoles_dir)
            file_path = os.path.join(
                consoles_dir,
                "_".join((x.rstrip("/").split("/")[-2:])) + ".gz")
            if os.path.exists(file_path):
                log.debug("Using cached Jenkins console: %s", file_path)
                with gzip.open(file_path, "rt") as f:
                    return f.read()
            elif os.path.exists(file_path+ "_404"):
                log.debug("Jenkins console cache is 404: %s", file_path)
                return None
            full_url = x + "/" + "consoleText"
            www = Web(full_url, timeout=5)
            page = www.get()
            if page and page.status_code == 404:
                log.error("Jenkins console has 404 error: %s", full_url)
                open(file_path + "_404", 'a').close()
            elif page:
                with gzip.open(file_path, "wt") as f:
                    f.write(page.text)
                log.debug("Saved jenkins console cache to: %s", file_path)
                return page.content.decode('utf-8')
            else:
                log.error("Failed to get Jenkins console: %s", full_url)
                return None

        def _extract_log_url(text):
            if RDO_RE.search(text):
                return RDO_RE.search(text).group(1)

        jobs = []
        text = comment['message']
        timestamp = datetime.datetime.fromtimestamp(comment['timestamp'])
        pipeline = (PIPE_RE.search(text).group(1)
                    if PIPE_RE.search(text) else '')
        data = JOB_RE.findall(text)
        if data:
            patch_num = PATCH_RE.search(text).group(1)
            patchset = [s for s in self.sets if s.number == int(patch_num)][0]
            for j in data:
                job = Job(
                    name=j[0],
                    log_url=j[1],
                    status=j[2],
                    length=parse_time(j[3]),
                    patch=self,
                    patchset=patchset,
                    timestamp=timestamp,
                    pipeline=pipeline
                )
                jobs.append(job)
        data2 = JOB_RE2.findall(text)
        if data2:
            patch_num = PATCH_RE.search(text).group(1)
            patchset = [s for s in self.sets if s.number == int(patch_num)][0]
            for j in data2:
                log_console = _get_jenkins_console(j[1])
                if not log_console:
                    continue
                log_url = _extract_log_url(log_console)
                if not log_url:
                    continue
                job = Job(
                    name=j[0],
                    log_url=log_url,
                    status=j[2],
                    length=parse_time(j[3]),
                    patch=self,
                    patchset=patchset,
                    timestamp=timestamp,
                        pipeline=pipeline
                )
                jobs.append(job)
        return jobs

    def get_jobs(self):
        res = []
        for comment in self.comments:
            res += self._extract_job_from_comment(comment)
        return res


class Patchset(object):
    """Patchset object

        Class that creates Patchset object from patchset data from gerrit.
        It contains various info the could be useful for reports.
    """
    def __init__(self, data, patch):
        self.number = int(data['number'])
        self.patchset_ctime = datetime.datetime.fromtimestamp(
            data['createdOn'])
        self.ref = data['ref']
        self.patchset_url = ('https://review.openstack.org/#/c/' +
                             patch['number'] + "/" + data['number'])


class Job(object):
    """Job object

        Class that creates Job object from patch data from gerrit.
        It's extracted from all comments to patch that are done by Jenkins.
        It contains various info the could be useful for reports.
    """

    def __init__(self, name, log_url, status, length, patch, patchset,
                 timestamp, pipeline=''):
        self.name = name
        self.log_url = log_url
        self.fail = status == 'FAILURE'
        self.status = status
        self.length = length
        self.patch = patch
        self.patchset = patchset
        self.ts = timestamp
        self.branch = self.patch.branch if self.patch else ""
        self.datetime = self._to_utc(self.ts).strftime("%Y-%m-%d %H:%M")
        self.log_hash = self.hashed(self.log_url)
        self.periodic = False
        self.pipeline = pipeline

    def hashed(self, url):
        return url.strip("/").split("/")[-1]

    def _to_utc(self, ts):
        return ts - UTC_OFFSET

    def __repr__(self):
        return str({'name': self.name,
                    'log_url': self.log_url,
                    'status': self.status,
                    'project': self.patch.project if self.patch else "",
                    'branch': self.branch,
                    'length': str(self.length),
                    'patchset': str(
                        self.patchset.number) if self.patchset else "",
                    'patchset_url': str(
                        self.patchset.patchset_url) if self.patchset else "",
                    'date': datetime.datetime.strftime(self.ts, "%m-%d %H:%M")
                    })
