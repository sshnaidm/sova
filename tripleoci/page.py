import jinja2
import os
import pickle

from tripleoci import config
from tripleoci.watchcat import meow
from tripleoci.utils import top, statistics, get_circles
from tripleoci.config import PLUGIN, TRIPLEOCI, RDOCI

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
        if PLUGIN == TRIPLEOCI:
            periodic_data = meow(limit=None,
                                 days=config.PERIODIC_DAYS,
                                 job_type=None,
                                 exclude=None,
                                 down_path=config.DOWNLOAD_PATH,
                                 periodic=True,
                                 fail=False)
            ci_data = meow(limit=None,
                           days=config.GATE_DAYS,
                           job_type=None,
                           fail=False,
                           down_path=config.DOWNLOAD_PATH)

            with open(
                    os.path.join(config.DOWNLOAD_PATH, "ci_data_dump"),
                    "wb") as g:
                pickle.dump(ci_data, g)
            with open(os.path.join(config.DOWNLOAD_PATH, "periodic_data_dump"),
                      "wb") as g:
                pickle.dump(periodic_data, g)
        elif PLUGIN == RDOCI:
            ci_data = meow(limit=None,
                           days=config.GATE_DAYS,
                           job_type=None,
                           exclude=None,
                           down_path=config.DOWNLOAD_PATH,
                           fail=False)

            periodic_data = []
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
    jobs_by_column = [{
        c: list(set(
            [i['job'].name for i in ci_data if p in i['job'].name]
        ))} for j in config.COLUMNS for c, p in j.items() ]
    columned = [k for j in jobs_by_column for i in j.values() for k in i]
    jobs_by_column.append({
        'Others': list(set([
        z['job'].name for z in ci_data if z['job'].name not in columned]
        ))})
    html = template.render({
        "ci": by_job_type(list(ci_data)),
        "periodic": by_job_type(list(periodic_data)),
        'ci_stats': stats,
        'periodic_stats': per_stats,
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
