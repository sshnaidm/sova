import fileinput
import re

from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()  # noqa

from tripleoci.config import log
from tripleoci.patterns import PATTERNS
from tripleoci.utils import JobFile, urlize_logstash

DEBUG = False


def analyze_all(jobs, down_path):
    p = Pool(50)
    results = []
    for k, j in enumerate(jobs):
        results.append(p.spawn(analyze, j, down_path, k))
    p.join()
    return [i.get() for i in results]


def analyze(job, down_path, num):
    def line_match(pat, line, exclude=None):
        exclude = exclude or []
        if any([i in line for i in exclude]):
            return False
        if isinstance(pat, re._pattern_type):
            if not pat.search(line):
                return False
            elif pat.search(line).groups():
                return pat.search(line).group(1)
            else:
                return True
        if isinstance(pat, str):
            return pat in line

    def compile_logstash(line, pat_stash):
        if isinstance(pat_stash, re._pattern_type):
            return 'message:"' + pat_stash.search(line).group() + '"'
        else:
            return 'message:"' + pat_stash + '"'

    log.debug("Starting task {}".format(num))
    message = {
        "text": '',
        "tags": set(),
        "msg": dict(),
        "reason": True,
        "job": job,
        "periodic": "periodic" in job.name,
        'patterns': set(),
        'logstash_url': set(),
        'success': job.status == 'SUCCESS',
    }
    templ = ("{date}\t"
             "{job_type:38}\t"
             "{delim}\t"
             "{msg:60}\t"
             "{delim}\t"
             "log: {log_url}")

    msg = dict()
    console = JobFile(job, path=down_path, offline=DEBUG).get_file()
    if not console:
        message['text'] = 'No console file'
        message['msg'] = {'No console file': 'infra'}
        message['tags'] = ['infra']
        return message
    if message['success']:
        message['text'] = 'SUCCESS'
        message['msg'] = {'SUCCESS': ''}
        message['reason'] = False
        message['tags'] = ['']
        return message
    files = PATTERNS.keys()
    for file in files:
        jfile = JobFile(job, path=down_path, file_link=file, offline=DEBUG
                        ).get_file()
        if not jfile:
            log.warn("File {} is not downloaded, "
                     "skipping its patterns".format(file))
            continue
        else:
            try:
                log.debug("Opening file for scan: {}".format(jfile))
                finput = fileinput.FileInput(
                    jfile, openhook=fileinput.hook_compressed)
                for line in finput:
                    line = line.decode()
                    for p in PATTERNS[file]:
                        line_matched = (line_match(
                            p["pattern"], line, exclude=p.get("exclude")
                        ) and p["msg"].lower() not in [i.lower() for i in msg])
                        if line_matched:
                            log.debug("Found pattern {} in file {}:{}".format(
                                repr(p), file, jfile))
                            msg.update({p["msg"].format(
                                line_match(p["pattern"], line)): p["tag"]})
                            message['tags'].add(p["tag"])
                            message['patterns'].add(p['id'])
                            if p['logstash']:
                                message['logstash_url'].add(compile_logstash(
                                    line, p['logstash']))
                finput.close()

            except Exception as e:
                log.error("Exception when parsing {}: {}".format(
                    jfile, str(e)))
                msg = {"Error when parsing logs.": 'info'}
                message['reason'] = False
                message['tags'].add("info")
    if not msg:
        log.debug("No patterns in job files {}".format(job))
        msg = {"Reason was NOT FOUND.": 'info'}
        message['reason'] = False
        message['tags'].add("info")
    if not [i for i in message['tags'] if i not in ('info', '')]:
        message['reason'] = False
        msg.update({"Please investigate.": 'info'})
    message['msg'] = msg
    message['logstash_url'] = urlize_logstash(message['logstash_url'])
    message['text'] = templ.format(
        msg=" ".join(sorted(msg)),
        delim="||" if message['reason'] else "XX",
        date=job.datetime,
        job_type=job.name,
        log_url=job.log_url
    )
    return message
