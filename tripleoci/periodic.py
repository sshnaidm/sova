import datetime
import json
import re

import tripleoci.config as config
from tripleoci.config import log
from tripleoci.patches import Job
from tripleoci.utils import Web

# Jobs regexps
branch_re = re.compile(r"\+ export ZUUL_BRANCH=(\S+)")
ts_re = re.compile(r"(201\d-[01]\d-[0123]\d [012]\d:\d\d):\d\d\.\d\d\d")
pipe_re = re.compile(r'  Pipeline: (.+)')
dlrnapi_success_re = re.compile('--success (true|false)')


class Periodic(object):
    """Periodic job object

        Class that actually parses periodic jobs HTML page.
        It tries to extract all available info from the page, but
        some info could be found only in console.html, for example
        job status. So it needs to download console.html for every job and
        to parse it also.
    """
    def __init__(self, down_path=config.DOWNLOAD_PATH, limit=None, pages=2):
        self.down_path = down_path
        self.limit = limit
        self.pages = pages
        self.jobs = self.get_jobs()

    def _get_list(self):
        result = []
        for per_url in config.PERIODIC_LOGS_URL:
            for page in range(self.pages):
                url = per_url + ('&skip=%d' % int(page * 50) if page else '')
                web = Web(url=url)
                req = web.get()
                if req is None or int(req.status_code) != 200:
                    log.warning("Trying again to download periodic page {}"
                                "".format(url))
                    req = web.get()
                    if req is None or int(req.status_code) != 200:
                        log.error(
                            "Can not retrieve periodic page {}".format(url))
                        continue
                try:
                    result += req.json()
                except json.decoder.JSONDecodeError as e:
                    log.error("Can't parse JSON of %s: %s" % (url, e))
        return result

    def _parse_ts(self, ts):
        return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")

    def parse_jobs(self, jobs_list):
        # Filter out jobs without logs
        filtered_jobs_list = [i for i in jobs_list if i.get('log_url') and
                              'http' in i['log_url']]
        jobs = [
            {
                'name': job['job_name'],
                'log_url': job['log_url'],
                'status': job['result'],
                'length': job['duration'],
                'ts': self._parse_ts(job['end_time']),
                'pipeline': job['pipeline']
            } for job in filtered_jobs_list
        ]
        return jobs

    def get_jobs(self):
        index = self._get_list()
        if index:
            jobs = self.parse_jobs(index)[:self.limit]
        else:
            jobs = []
        for j in jobs:
            yield PeriodicJob(**j)


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
