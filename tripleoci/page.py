import jinja2
import os
import pickle

from tripleoci import config
from tripleoci.watchcat import meow
from tripleoci.utils import top, statistics

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

    work_dir = os.path.dirname(__file__)
    if not DEBUG:
        ci_data = meow(limit=None,
                       days=8,
                       job_type=None,
                       fail=False,
                       down_path=config.DOWNLOAD_PATH)

        periodic_data = meow(limit=None,
                             days=14,
                             job_type=None,
                             exclude=None,
                             down_path=config.DOWNLOAD_PATH,
                             periodic=True,
                             fail=False)

        with open(
                os.path.join(config.DOWNLOAD_PATH, "ci_data_dump"), "wb") as g:
            pickle.dump(ci_data, g)
        with open(os.path.join(config.DOWNLOAD_PATH, "periodic_data_dump"),
                  "wb") as g:
            pickle.dump(periodic_data, g)
    # For debug mode
    else:
        with open(
                os.path.join(config.DOWNLOAD_PATH, "ci_data_dump"), "rb") as g:
            ci_data = pickle.load(g)
        with open(os.path.join(config.DOWNLOAD_PATH, "periodic_data_dump"),
                  "rb") as g:
            periodic_data = pickle.load(g)

    errors_top = top(ci_data)
    stats, per_stats = statistics(ci_data), statistics(
        periodic_data)

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

    html = template.render({
        "ci": by_job_type(list(ci_data)),
        "periodic": by_job_type(list(periodic_data)),
        'ci_stats': stats,
        'periodic_stats': per_stats,
        "errors_top": errors_top,
        "branches": branches,
    })
    with open(config.INDEX_HTML, "w") as f:
        # f.write(html.encode('utf-8'))
        f.write(html.encode('ascii', 'ignore').decode('ascii'))


def main():
    create_html()


if __name__ == '__main__':
    main()
