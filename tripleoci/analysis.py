import fileinput
import re

from tripleoci.config import log
from tripleoci.patterns import PATTERNS
from tripleoci.utils import JobFile

DEBUG = False

def analyze(job, down_path):
    def line_match(pat, line):
        if isinstance(pat, re._pattern_type):
            if not pat.search(line):
                return False
            elif pat.search(line).groups():
                return pat.search(line).group(1)
            else:
                return True
        if isinstance(pat, str):
            return pat in line

    message = {
        "text": '',
        "tags": set(),
        "msg": set(),
        "reason": True,
        "job": job,
        "periodic": "periodic" in job.name,
        'patterns': set(),
    }
    templ = ("{date}\t"
             "{job_type:38}\t"
             "{delim}\t"
             "{msg:60}\t"
             "{delim}\t"
             "log: {log_url}")

    msg = set()
    console = JobFile(job, path=down_path, offline=DEBUG).get_file()
    if not console:
        message['text'] = 'No console file'
        message['msg'] = set(message['text'])
        message['tags'] = ['infra']
        message['reason'] = True
        return message
    files = PATTERNS.keys()
    for file in files:
        jfile = JobFile(job, path=down_path, file_link=file, offline=DEBUG
                        ).get_file()
        if not jfile:
            log.error("File {} is not downloaded, "
                      "skipping its patterns".format(file))
            continue
        else:
            try:
                log.debug("Opening file for scan: {}".format(jfile))
                for line in fileinput.input(
                        jfile, openhook=fileinput.hook_compressed):
                    line = line.decode()
                    for p in PATTERNS[file]:
                        if (line_match(p["pattern"], line) and
                                p["msg"] not in msg):
                            log.debug("Found pattern {} in file {}:{}".format(
                                repr(p), file, jfile))
                            msg.add(p["msg"].format(
                                line_match(p["pattern"], line)))
                            message['tags'].add(p["tag"])
                            message['patterns'].add(p['id'])

            except Exception as e:
                log.error("Exception when parsing {}: {}".format(
                    jfile, str(e)))
                msg = {"Error when parsing logs. Please investigate"}
                message['reason'] = False
                message['tags'].add("unknown")
    if not msg:
        log.debug("No patterns in job files {}".format(job))
        msg = {"Reason was NOT FOUND. Please investigate"}
        message['reason'] = False
        message['tags'].add("unknown")
    message['msg'] = msg
    message['text'] = templ.format(
        msg=" ".join(sorted(msg)),
        delim="||" if message['reason'] else "XX",
        date=job.datetime,
        job_type=job.name,
        log_url=job.log_url
    )
    return message
