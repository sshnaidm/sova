import datetime
import re
import time

JOB_RE = re.compile(r"(\S+) (http://logs.openstack.org/\S+) "
                    r": (FAILURE|SUCCESS) in ([hms \d]+)")
PATCH_RE = re.compile(r"Patch Set (\d+):")
TIME_RE = re.compile(r"((?P<hour>\d+)h)? *((?P<min>\d+)m)? *((?P<sec>\d+)s)?")


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

        jobs = []
        text = comment['message']
        timestamp = datetime.datetime.fromtimestamp(comment['timestamp'])
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
                    timestamp=timestamp
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
    def __init__(self,
                 name, log_url, status, length, patch, patchset, timestamp):
        self.name = name
        self.log_url = log_url
        self.fail = status == 'FAILURE'
        self.status = status
        self.length = length
        self.patch = patch
        self.patchset = patchset
        self.ts = timestamp
        self.branch = self.patch.branch if self.patch else ""
        self.datetime = self._to_utc(self.ts).strftime("%m-%d %H:%M")
        self.log_hash = self.hashed(self.log_url)
        self.periodic = False

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
