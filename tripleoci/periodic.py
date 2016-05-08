import datetime
import os
import gzip
import fileinput
import re
from lxml import etree

import config
from config import log
from patches import Job
from utils import Web

# Jobs regexps
branch_re = re.compile(r"\+ export ZUUL_BRANCH=(\S+)")
ts_re = re.compile(r"(201\d-[01]\d-[0123]\d [012]\d:\d\d):\d\d\.\d\d\d")


class Periodic(object):
    """
        Class that actually parses periodic jobs HTML page.
        It tries to extract all available info from the page, but
        some info could be found only in console.html, for example
        job status. So it needs to download console.html for every job and
        to parse it also.
    """
    def __init__(self, url, down_path=config.DOWNLOAD_PATH, limit=None):
        self.per_url = url
        self.down_path = down_path
        self.limit = limit
        self.jobs = self.get_jobs()

    def _get_index(self):
        web = Web(self.per_url)
        req = web.get()
        if req.status_code != 200:
            log.error("Can not retrieve periodic page {}".format(self.per_url))
            return None
        return req.content

    def _get_console(self, job):
        path = os.path.join(
            self.down_path, job["log_hash"], "console.html.gz")
        if os.path.exists(path):
            log.debug("Console is already here: {}".format(path))
            return path
        web = Web(job["log_url"] + "/console.html")
        req = web.get(ignore404=True)
        if req.status_code == 404:
            url = job["log_url"] + "/console.html.gz"
            web = Web(url=url)
            log.debug("Trying to download gzipped console")
            req = web.get()
        if req.status_code != 200:
            log.error("Failed to retrieve console: {}".format(job["log_url"]))
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
            job = {}
            td1, td2 = tr.xpath("td")[1:3]
            lhash = td1.xpath("a")[0].attrib['href'].rstrip("/")
            job["log_hash"] = lhash
            job["log_url"] = self.per_url.rstrip("/") + "/" + lhash
            job["ts"] = datetime.datetime.strptime(td2.text.strip(),
                                                   "%d-%b-%Y %H:%M")
            job["name"] = self.per_url.rstrip("/").split("/")[-1]
            jobs.append(job)
        return sorted(jobs, key=lambda x: x['ts'], reverse=True)

    def _parse_ts(self, ts):
        return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M")

    def _get_more_data(self, j):
        def delta(e, s):
            return (self._parse_ts(e) - self._parse_ts(s)).seconds / 60

        start = end = None
        j.update({
            'status': 'FAILURE',
            'fail': True,
            'branch': ''
        })
        console = self._get_console(j)
        if not console:
            log.error("Failed to get console for periodic {}".format(repr(j)))
        else:
            for line in fileinput.input(console,
                                        openhook=fileinput.hook_compressed):
                if "Finished: SUCCESS" in line:
                    j['fail'] = False
                    j['status'] = 'SUCCESS'
                elif "Finished: FAILURE" in line:
                    j['fail'] = True
                    j['status'] = 'FAILURE'
                elif "Finished: ABORTED" in line:
                    j['fail'] = True
                    j['status'] = 'ABORTED'
                if branch_re.search(line):
                    j['branch'] = branch_re.search(line).group(1)
                if 'Started by user' in line:
                    start = ts_re.search(line).group(1)
                if "Finished: " in line:
                    end = ts_re.search(line).group(1)
            j['length'] = delta(end, start) if start and end else 0
        return j

    def get_jobs(self):
        index = self._get_index()
        jobs = self.parse_index(index)[:self.limit]
        for j in jobs:
            raw = self._get_more_data(j)
            yield PeriodicJob(**raw)


class PeriodicJob(Job):
    """
        Class that contains all necessary info for periodic job.
    """
    def __init__(self, **kwargs):
        super(PeriodicJob, self).__init__(
            name=kwargs["name"],
            log_url=kwargs["log_url"],
            status=kwargs["status"],
            length=kwargs["length"],
            timestamp=kwargs["ts"],
            patch=None,
            patchset=None
        )
        self.periodic = True
