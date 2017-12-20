import jinja2
import os
import pickle

from tripleoci import config
from tripleoci.utils import get_circles
from tripleoci.utils import statistics
from tripleoci.utils import top
from tripleoci.watchcat import meow


DEBUG = False


def create_html():
    """Create HTML page

        This function runs job analysis by calling meow() and creates HTML page
        with all data it received.
        HTML is created by Jinja templating template.html file.

    :return: writes index.html file in current directory
    """

    def by_job_type(l):
        job_types = {i["job"].name for i in l if i["job"].name}
        d = {}
        for job_type in job_types:
            d[job_type] = [i for i in l if i["job"].name == job_type]
        return d

    work_dir = config.TEMPLATE_DIR
    if not DEBUG:
        ci_data = []
        # ci_data = meow(limit=None,
        #                days=config.GATE_DAYS,
        #                job_type=None,
        #                fail=False,
        #                down_path=config.DOWNLOAD_PATH)

        periodic_data = meow(limit=None,
                             days=config.PERIODIC_DAYS,
                             job_type=None,
                             exclude=None,
                             down_path=config.DOWNLOAD_PATH,
                             periodic=True,
                             fail=False)
        ci_data += periodic_data

        with open(
                os.path.join(config.DOWNLOAD_PATH, "ci_data_dump"), "wb") as g:
                pickle.dump(ci_data, g)
    # For debug mode
    else:
        with open(
                os.path.join(config.DOWNLOAD_PATH, "ci_data_dump"), "rb") as g:
                ci_data = pickle.load(g)

    errors_top = top(ci_data)
    stats = statistics(ci_data)
    circles = get_circles(ci_data)

    JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(work_dir),
        extensions=['jinja2.ext.autoescape',
                    'jinja2.ext.do',
                    'jinja2.ext.loopcontrols'],
        autoescape=True)
    template = JINJA_ENVIRONMENT.get_template('template.html')
    branches = sorted(
        set([i['job'].branch.replace("stable/", "") for i in ci_data] +
            [i.replace("stable/", "") for i in config.GERRIT_BRANCHES]))
    all_job_names = set([i['job'].name for i in ci_data])
    jobs_by_column = sorted([(i, [os.path.basename(k) for k in j if
                                  os.path.basename(k) in all_job_names])
                             for i, j in config.COLUMNED_TRACKED_JOBS.items()],
                            key=lambda x: len(x[1]), reverse=True)
    empty_jobs = [os.path.basename(i)
                  for k in config.COLUMNED_TRACKED_JOBS.values()
                  for i in k if os.path.basename(i) not in all_job_names]

    if empty_jobs:
        print("Empty jobs:", ", ".join(empty_jobs))
    html = template.render({
        "ci": by_job_type(list(ci_data)),
        'ci_stats': stats,
        "errors_top": errors_top,
        "branches": branches,
        "jobs_by_column": jobs_by_column,
        "circles": circles
    })
    with open(config.INDEX_HTML, "w") as f:
        # f.write(html.encode('utf-8'))
        f.write(html.encode('ascii', 'ignore').decode('ascii'))


def main():
    create_html()


if __name__ == '__main__':
    main()
