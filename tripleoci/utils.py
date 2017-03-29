import contextlib
import datetime
import gzip
import json
import os
import paramiko
import requests
import tarfile
import time

from backports import lzma
from collections import Counter
from requests import ConnectionError
from six.moves.urllib.parse import quote
import tripleoci.config as config
from tripleoci.config import log

requests.packages.urllib3.disable_warnings()


class SSH(object):
    """SSH

        SSH class, just for any connection
    """

    def __init__(self,
                 host, port, user, timeout=None, key=None, key_path=None):
        self.ssh_cl = paramiko.SSHClient()
        self.ssh_cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        log.debug("Executing ssh {user}@{host}:{port}".format(
            user=user, host=host, port=port))
        self.ssh_cl.connect(hostname=host,
                            port=port,
                            username=user,
                            timeout=timeout,
                            pkey=key,
                            key_filename=key_path)

    def exe(self, cmd):
        log.debug("Executing cmd by ssh: {cmd}".format(cmd=cmd))
        try:
            stdin, stdout, stderr = self.ssh_cl.exec_command(cmd)
        except paramiko.ssh_exception.SSHException as e:
            log.error("SSH command failed: {}\n{}".format(cmd, e))
            return None, None, None
        except EOFError as e:
            log.error("SSH command failed with: {}\n{}".format(cmd, e))
            return None, None, None
        return stdin, stdout.read(), stderr.read()

    def close(self):
        log.debug("Closing SSH connection")
        self.ssh_cl.close()


class Gerrit(object):
    """Get Gerrit changes

        Gerrit class, it connects to upstream Gerrit and run queries.
        It downloads all info about patches from given projects.
    """

    def __init__(self, period=None):
        self.key_path = config.SSH_PRIV_KEY
        self.ssh = None
        self.period = period

    def get_project_patches(self, projects):
        def filtered(x):
            return [json.loads(i.decode(errors='ignore'))
                    for i in x.splitlines()
                    if 'project' in i.decode(errors='ignore')]

        def calc_date(x):
            return (
                datetime.datetime.today() - datetime.timedelta(days=x)
            ).date().strftime("%Y-%m-%d")

        data = []

        cmd_template = ('gerrit query "status: reviewed project: '
                        '{project} '
                        'branch: {branch}" '
                        '--comments '
                        '--format JSON '
                        'limit: {limit} '
                        '--patch-sets '
                        '--current-patch-set')
        if self.period:
            cmd_template += ' after:"{date}"'.format(
                date=calc_date(self.period))
        for proj in projects:
            # Start SSH for every project from scratch because SSH timeout
            self.ssh = SSH(host=config.GERRIT_HOST,
                           port=config.GERRIT_PORT,
                           user=config.GERRIT_USER,
                           timeout=config.GERRIT_REQ_TIMEOUT,
                           key_path=self.key_path)
            for branch in config.GERRIT_BRANCHES:
                command = cmd_template.format(
                    project=proj,
                    branch=branch,
                    limit=config.GERRIT_PATCH_LIMIT)
                out, err = self.ssh.exe(command)[1:]
                if err:
                    log.error("Error with ssh:{}".format(err))
                real_data = filtered(out) if out else []
                log.debug("Length of result is {}".format(len(real_data)))
                data += real_data
            self.ssh.close()
            # Let's not ddos Gerrit
            time.sleep(1)
        return data


class Web(object):
    """Download web page

        Web class for downloading web page
    """

    def __init__(self, url):
        self.url = url

    def get(self, ignore404=False):
        """Get web file

            Sometimes console.html is gzipped on logs server and console.html
            is not available anymore, so here it silently fails when trying to
            download console.html and then tries to get console.html.gz
            We don't want redundant error messages in console

        :param ignore404: not to show error message if got 404 error
        :return: request obj
        """
        log.debug("GET {url} with ignore404={i}".format(
            url=self.url, i=str(ignore404)))
        try:
            req = requests.get(self.url, timeout=config.WEB_TIMEOUT)
        except ConnectionError:
            log.error("Connection error when retriving {}".format(self.url))
            return None
        except Exception as e:
            log.error("Unknown error when retriving {}: {}".format(
                self.url, str(e)))
            try:
                req = requests.get(self.url, timeout=config.WEB_TIMEOUT_LATE)
            except Exception as e:
                log.error("Giving up with error {}: {}".format(
                    self.url, str(e)))
                return None
        if int(req.status_code) != 200:
            if not (ignore404 and int(req.status_code) == 404):
                log.warn("Page {url} got status {code}".format(
                    url=self.url, code=req.status_code))
        return req


class JobFile(object):
    """Get files of job

        JobFile downloads file from saved logs of the job.
        It supports two modes: gzipped flat file and file from *.tar.xz.
        If we need /var/log/neutron/server.log from overcloud-control.tar.xz
        file then we pass link as:
        /logs/overcloud-control.tar.gz//var/log/neutron/server.log
        It tells to download overcloud-control.tar.xz from saved logs, then
        extracts var/log/neutron/server.log to created 'overcloud-control'
        folder and save it gzipped.
        The flat file is also saved gzipped to save the space on disk.
        All files related to job are saved in job directory that named as log
        hash in URL to prevent collisions.
        If file presents on disk it doesn't download it.
    """

    def __init__(self, job, path=config.DOWNLOAD_PATH, file_link=None,
                 build=None, offline=False):
        self.job_dir = os.path.join(path, job.log_hash)
        if not os.path.exists(self.job_dir):
            os.makedirs(self.job_dir)
        # /logs/undercloud.tar.gz//var/log/nova/nova-compute.log
        self.file_link = file_link or "console.html"
        self.file_url = job.log_url + self.file_link.split("//")[0]
        self.file_path = None
        self.build = build
        self.file_name = None
        self.offline = offline

    def get_file(self):
        '''Get file

        Double slash "//" means we need to download tar.xz and then
           to extract file after "//" from it:
                /logs/overcloud-controller-0.tar.xz//var/log/neutron/server.log
        :return: path to gzipped file
        '''
        if self.offline:
            return self.dummy_file()
        if self.build:
            return self.get_build_page()
        if "//" in self.file_link:
            return self.get_tarred_file()
        else:
            return self.get_regular_file()

    def dummy_file(self):
        if "//" in self.file_link:
            tar_file_link, intern_path = self.file_link.split("//")
            tar_base_name = os.path.basename(tar_file_link)
            tar_prefix = tar_base_name.split(".")[0]
            tar_root_dir = os.path.join(self.job_dir, tar_prefix)
            self.file_path = os.path.join(tar_root_dir, intern_path)
        else:
            self.file_name = os.path.basename(
                self.file_link).split(".gz")[0] + ".gz"
            self.file_path = os.path.join(self.job_dir, self.file_name)
        return self.file_path if os.path.exists(self.file_path) else None

    def get_build_page(self):
        web = Web(url=self.build)
        req = web.get()
        if req is None:
            log.error("Jenkins page {} is unavailable".format(self.build))
            return None
        if int(req.status_code) != 200:
            return None
        else:
            self.file_path = os.path.join(self.job_dir, "build_page.gz")
            with gzip.open(self.file_path, "wt") as f:
                f.write(req.text)
            return self.file_path

    def get_regular_file(self):
        log.debug("Get regular file {}".format(self.file_link))
        self.file_name = os.path.basename(
            self.file_link).split(".gz")[0] + ".gz"
        self.file_path = os.path.join(self.job_dir, self.file_name)
        if os.path.exists(self.file_path):
            log.debug("File {} is already downloaded".format(self.file_path))
        else:
            if "." not in self.file_url.split("/")[-1]:
                file_try1 = self.file_url
            else:
                file_try1 = self.file_url + ".gz"
            web = Web(url=file_try1)
            req = web.get(ignore404=True)
            if req is None:
                log.warn("Failed to retrieve URL, request is None: {}".format(
                         file_try1))
                return None
            elif int(req.status_code) == 404:
                if self.file_url.endswith(".html"):
                    file_try2 = self.file_url
                elif self.file_url.endswith(".txt"):
                    file_try2 = self.file_url[:-4] + ".log"
                else:
                    log.warn("Failed to retrieve URL, tried once: {}".format(
                        file_try1))
                    return None
                web = Web(url=file_try2)
                log.debug("Trying to download raw file {}".format(file_try2))
                req = web.get()
                if req is None or int(req.status_code) != 200:
                    log.warn("Failed to retrieve URL, tried twice: {}".format(
                        file_try2))
                    return None
            elif int(req.status_code) not in (200, 404):
                log.warn(
                    "Failed to retrieve URL, request failure: {} {}".format(
                        file_try1, req.status_code))
                return None
            if int(req.status_code) == 200:
                with gzip.open(self.file_path, "wt") as f:
                    f.write(req.text)
        return self.file_path

    def _extract(self, tar, root_dir, file_path):
        log.debug("Extracting file {} from {} in {}".format(
            file_path, tar, root_dir))
        try:
            with contextlib.closing(lzma.LZMAFile(tar)) as xz:
                with tarfile.open(fileobj=xz) as f:
                    f.extract(file_path, path=root_dir)
            return True
        except Exception as e:
            log.error("Error when untarring file {} from {} in {}:{}".format(
                file_path, tar, root_dir, e))
            return False

    def get_tarred_file(self):
        tar_file_link, intern_path = self.file_link.split("//")
        log.debug("Get file {} from tar.gz archive {}".format(intern_path,
                                                              tar_file_link))
        tar_base_name = os.path.basename(tar_file_link)
        tar_prefix = tar_base_name.split(".")[0]
        tar_root_dir = os.path.join(self.job_dir, tar_prefix)
        self.file_path = os.path.join(tar_root_dir, intern_path)

        if os.path.exists(self.file_path + ".gz"):
            log.debug("File {} is already downloaded".format(
                self.file_path + ".gz"))
            return self.file_path + ".gz"
        if not os.path.exists(tar_root_dir):
            os.makedirs(tar_root_dir)
        tar_file_path = os.path.join(self.job_dir, tar_base_name)
        if not os.path.exists(tar_file_path):
            web = Web(url=self.file_url)
            req = web.get()
            if req is None or int(req.status_code) != 200:
                return None
            else:
                with open(tar_file_path, "w") as f:
                    f.write(req.text)
        if self._extract(tar_file_path, tar_root_dir, intern_path):
            with open(self.file_path, 'r') as f:
                with gzip.open(self.file_path + ".gz", 'wt') as zipped_file:
                    zipped_file.writelines(f)
            os.remove(self.file_path)
            self.file_path += ".gz"
            return self.file_path
        else:
            return None


def top(data):
    msgs = [j for i in data
            for j in i['msg'] if i['msg'][j] not in ('info', '')]
    xtop = Counter(msgs)
    return xtop.most_common()


def statistics(data):

    def calc_today_str():
        return datetime.date.today().strftime("%m-%d")

    def calc_yesterday_str():
        return (datetime.datetime.today() - datetime.timedelta(days=1)
                ).date().strftime("%m-%d")

    def calc_week():
        return [(datetime.datetime.today() -
                 datetime.timedelta(days=i)).date().strftime("%m-%d")
                for i in range(7)]

    chart_data = []
    for job in data:
        if job['job'].status == 'SUCCESS':
            chart_category = 'succ'
        elif 'infra' in job['tags']:
            chart_category = 'infra'
        elif 'code' in job['tags']:
            chart_category = 'code'
        else:
            chart_category = 'unknown'
        # Take only first part from "'11-09 22:24'"
        chart_date = job['job'].datetime.split()[0]
        chart_name = job['job'].name
        chart_period = job['periodic']
        chart_data.append({
            'category': chart_category,
            'date': chart_date,
            'name': chart_name,
            'periodic': chart_period,
            "uuid": chart_name + "_" + "_".join(job['job'].datetime.split())
        })
    all_statistics = dict(Counter([i['category'] for i in chart_data]))

    names = set([i['name'] for i in chart_data])
    all_by_job_name = {}
    for name in names:
        all_by_job_name[name] = [i for i in chart_data if i['name'] == name]

    job_by_name = {}
    for name in names:
        job_by_name[name] = dict(
            Counter([i['category'] for i in all_by_job_name[name]]))

    dates = set([i['date'] for i in chart_data])
    all_by_date = {}
    for date in dates:
        all_by_date[date] = dict(
            Counter([i['category'] for i in chart_data if i['date'] == date]))

    jobs_by_date = {}
    for name in names:
        jobs_by_date[name] = {}
        for date in set([i['date'] for i in all_by_job_name[name]]):
            jobs_by_date[name][date] = dict(Counter(
                [i['category'] for i in all_by_job_name[name] if
                 i['date'] == date]))

    today_jobs = {}
    today = calc_today_str()
    for name in names:
        today_jobs[name] = dict(Counter([i['category'] for i in chart_data
                                         if i['date'] == today and
                                         i['name'] == name]))
    today_jobs_all = dict(Counter([i['category'] for i in chart_data
                                   if i['date'] == today]))
    yesterday_jobs = {}
    yesterday = calc_yesterday_str()
    for name in names:
        yesterday_jobs[name] = dict(Counter([i['category'] for i in chart_data
                                             if i['date'] == yesterday and
                                             i['name'] == name]))
    yesterday_jobs_all = dict(Counter([i['category'] for i in chart_data
                                       if i['date'] == yesterday]))
    week_jobs = {}
    week = calc_week()
    for name in names:
        week_jobs[name] = dict(Counter([i['category'] for i in chart_data
                                        if i['date'] in week and
                                        i['name'] == name]))
    week_jobs_all = dict(Counter([i['category'] for i in chart_data
                                  if i['date'] in week]))

    return {
        "all_statistics": all_statistics,
        "all_by_job_name": all_by_job_name,
        "all_by_date": all_by_date,
        "jobs_by_date": jobs_by_date,
        "today_jobs": today_jobs,
        "yesterday_jobs": yesterday_jobs,
        "job_by_name": job_by_name,
        "week_jobs": week_jobs,
        "today_jobs_all": today_jobs_all,
        "yesterday_jobs_all": yesterday_jobs_all,
        "week_jobs_all": week_jobs_all
    }


def urlize_logstash(msgs):
    msgs = [i for i in msgs if i]
    if not msgs:
        return None
    if len(msgs) > 1:
        msg = "(" + " OR ".join(msgs) + ")"
    else:
        msg = msgs[0]
    query = (msg +
             (' AND build_name:*tripleo-ci-* AND tags:console AND voting:1 '
              'AND build_status:FAILURE'))
    base_url = ('http://logstash.openstack.org/'
                '#/dashboard/file/logstash.json?query=')
    url = base_url + quote(query.replace('"', '\\"'))
    return url
