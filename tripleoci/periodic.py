import datetime
import fileinput
import gzip
import os
import re

from lxml import etree

import tripleoci.config as config
from tripleoci.config import log
from tripleoci.patches import Job
from tripleoci.utils import Web

# Jobs regexps
branch_re = re.compile(r"\+ export ZUUL_BRANCH=(\S+)")
ts_re = re.compile(r"(201\d-[01]\d-[0123]\d [012]\d:\d\d):\d\d\.\d\d\d")
pipe_re = re.compile(r'  Pipeline: (.+)')


class Periodic(object):
    """Periodic job object

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
        if req is None or int(req.status_code) != 200:
            log.warning(
                "Trying again to download periodic page ".format(self.per_url))
            req = web.get()
            if req is None or int(req.status_code) != 200:
                log.error(
                    "Can not retrieve periodic page {}".format(self.per_url))
                return None
        return req.content

    def _get_console(self, job):
        console_name = config.ACTIVE_PLUGIN_CONFIG.console_name
        if isinstance(console_name, list):
            console_name = console_name[0]
        path = os.path.join(
            self.down_path, job["log_hash"], console_name)
        if os.path.exists(path):
            log.debug("Console is already here: {}".format(path))
            return path

        console_names = config.ACTIVE_PLUGIN_CONFIG.console_name
        if not isinstance(console_names, list):
            console_names = [console_names]
        for console_name in console_names:
            web = Web(job["log_url"] + "/" + console_name, timeout=7)
            log.debug("Trying to download console: {}".format(
                      job["log_url"] + "/" + console_name))
            req = web.get(ignore404=True)
            if req is None or int(req.status_code) != 200:
                log.error("Failed to retrieve console: {}".format(
                    job["log_url"] + "/" + console_name))
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
            job = {}
            td1, td2 = tr.xpath("td")[1:3]
            lhash = td1.xpath("a")[0].attrib['href'].rstrip("/")
            job["log_hash"] = lhash
            job["log_url"] = self.per_url.rstrip("/") + "/" + lhash
            job["ts"] = datetime.datetime.strptime(td2.text.strip(),
                                                   "%Y-%m-%d %H:%M")
            job["name"] = self.per_url.rstrip("/").split("/")[-1]
            jobs.append(job)
        return sorted(jobs, key=lambda x: x['ts'], reverse=True)

    def _parse_ts(self, ts):
        return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M")

    def _get_more_data(self, j):
        def delta(e, s):
            return (self._parse_ts(e) - self._parse_ts(s)).seconds / 60

        start = end = last = None
        j.update({
            'status': 'FAILURE',
            'fail': True,
            'branch': '',
            'length': 0,
        })
        console = self._get_console(j)
        if not console:
            log.error("Failed to get console for job {}".format(repr(j)))
            return None
        else:
            finput = fileinput.FileInput(console,
                                         openhook=fileinput.hook_compressed)
            for line in finput:
                line = line.decode()
                if ('|  SUCCESSFULLY FINISHED' in line):
                    j['fail'] = False
                    j['status'] = 'SUCCESS'
                elif ('|  *** FAILED' in line):
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
                try:
                    if ('Started by user' in line or
                            '[Zuul] Launched by' in line or
                        '| PRE-RUN START' in line):
                        start = ts_re.search(line).group(1)
                    if ("|  Run completed" in line or
                       '[Zuul] Job complete' in line or
                        '| POST-RUN START' in line):
                        end = ts_re.search(line).group(1)
                except Exception as e:
                    log.error(e)
                    return None
                if ts_re.search(line):
                    last = ts_re.search(line).group(1)
            end = end or last
            j['length'] = delta(end, start) if start and end else 0
            j['ts'] = self._parse_ts(end) if end else j['ts']
            finput.close()
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
