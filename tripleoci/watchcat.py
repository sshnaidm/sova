from __future__ import print_function
import json
import tripleoci.config as config
from tripleoci.config import PLUGIN, TRIPLEOCI, RDOCI

from tripleoci.analysis import analyze_all
from tripleoci.filters import Filter
from tripleoci.patches import Patch
from tripleoci.periodic import Periodic
from tripleoci.rdoci import RDO_CI
from tripleoci.utils import Gerrit


DEBUG = False


def meow(days=None,
         dates=None,
         limit=None,
         short=None,
         fail=True,
         exclude=None,
         job_type=None,
         down_path=config.DOWNLOAD_PATH,
         periodic=False,
         ):
    """Main function

        This function actually runs the whole work,
        you can import it anywhere and run with parameters:

    :param days: how many days history to take, usually 7 (week) is enough
    :param dates: specific dates in format ["%m-%d", ..]: ['04-15', '05-02']
    :param limit: limit overall amount of jobs to analyze
    :param short: analyze only this type of jobs,
                    accepts short name: "ha","upgrades","nonha"
    :param fail: whether analyze and print only failed jobs (true by default)
    :param exclude: exclude specific job type: "gate-tripleo-ci-f22-containers"
    :param job_type: include only this job type (like short, but accepts
                        full name): "gate-tripleo-ci-f22-nonha"
    :param down_path: path on local system to save all jobs files there
    :param periodic: if take periodic (periodic=True) or patches (False)
    :return: parsed jobs data, ready for printing to HTML or console
    """

    if PLUGIN == TRIPLEOCI:
        if not periodic:
            if not DEBUG:
                g = Gerrit(period=days)
                gerrit = g.get_project_patches(config.PROJECTS)
                # Dump gerrit data for investigation
                with open(config.TMP_DIR + "/gerrit", "w") as f:
                    f.write(json.dumps(gerrit))
            # If debug mode
            else:
                with open(config.TMP_DIR + "/gerrit", "r") as f:
                    gerrit = json.loads(f.read())
            jobs = (job for patch in gerrit for job in Patch(patch).jobs)
        else:
            jobs = (job
                    for url in config.PERIODIC_URLS
                    for job in Periodic(
                        url, down_path=down_path, limit=limit).jobs)
    elif PLUGIN == RDOCI:
        jobs = (job
                for job in RDO_CI(down_path=down_path, limit=limit).jobs)
    f = Filter(
        jobs,
        days=days,
        dates=dates,
        limit=limit,
        short=short,
        fail=fail,
        exclude=exclude,
        job_type=job_type,
        periodic=periodic
    )
    filtered = f.run()
    ready = analyze_all(filtered, down_path=down_path)
    return ready


def main():
    for m in meow(limit=10, periodic=False):
        # print m["text"]
        print(m)


if __name__ == "__main__":
    main()
