import datetime
import re
import time
from tripleoci.config import log, CACHE_TIMEOUT
from tripleoci.utils import Web, cache


ZUUL_STATUSES = ["SUCCESS", "FAILURE", "RETRY_LIMIT", "POST_FAILURE",
                 "TIMED_OUT"]
JOB_REGEX = (
    re.compile(r"(\S+) (https://zuul.opendev.org/t/openstack/build/\S+) "
               r": (%s) in ([hms \d]+)" % "|".join(ZUUL_STATUSES)),
    re.compile(r"(\S+) (http://logs.rdoproject.org/\S+) "
               r": (%s) in ([hms \d]+)" % "|".join(ZUUL_STATUSES))
)
PATCH_RE = re.compile(r"Patch Set (\d+):")
TIME_RE = re.compile(r"((?P<hour>\d+)h)? *((?P<min>\d+)m)? *((?P<sec>\d+)s)?")
RDO_RE = re.compile(r'Logs have been uploaded and are available at:'
                    r'.*(https://logs.rdoproject.org/[^<>\s]+)', re.DOTALL)
PIPE_RE = re.compile(r"([^ \(\)]+) pipeline")
BUILD_ID = re.compile(r'https://zuul.opendev.org/t/openstack/build/(\S+)')


def utc_delta():
    ts = time.time()
    utc_offset = (datetime.datetime.fromtimestamp(ts) -
                  datetime.datetime.utcfromtimestamp(ts)).total_seconds()
    return datetime.timedelta(seconds=utc_offset)


UTC_OFFSET = utc_delta()


def add_log_url_to_cache(key, value):
    cache.set(key, value, expire=CACHE_TIMEOUT)
    log.debug("Added to cache URL %s", value)


def get_log_url_from_cache(key):
    if key in cache:
        url = cache[key]
        log.debug("Getting from cache URL %s", url)
        return url
    return None


def retrieve_log_from_swift(log_string):
    # RDO Zuul doesn't store in SWIFT, so it's a direct link to logs
    if "logs.rdoproject.org" in log_string:
        return log_string
    elif "zuul.opendev.org" in log_string:
        # retrieve JSON info from current link
        build_re = BUILD_ID.search(log_string)
        if build_re:
            build_id = build_re.group(1)
        else:
            # failed to parse URL
            log.error("Failed to parse URL=%s", log_string)
            return None
        log_url = ("https://zuul.opendev.org/api/tenant/openstack/build/%s"
                   % build_id)
        from_cache = get_log_url_from_cache(log_url)
        if from_cache:
            return from_cache
        web = Web(log_url)
        req = web.get()
        try:
            json_data = req.json()
        except Exception as e:
            log.error("Exception when decoding JSON from SWIFT URL of Zuul"
                      " %s: %s", log_url, str(e))
            return None
        job_log_url = json_data.get('log_url')
        if not job_log_url:
            log.error('log_url is not in data %s: %s', log_url, json_data)
            return None
        add_log_url_to_cache(log_url, job_log_url)
        return job_log_url
    else:
        # unknown log link
        log.error("Unknown log link: %s", log_string)
        return None


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
        pipeline = (PIPE_RE.search(text).group(1)
                    if PIPE_RE.search(text) else '')
        for regex in JOB_REGEX:
            data = regex.findall(text)
            if data:
                patch_num = PATCH_RE.search(text).group(1)
                patchset = [s for s in self.sets
                            if s.number == int(patch_num)][0]
                for j in data:
                    log_url = retrieve_log_from_swift(j[1]) or ''
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
