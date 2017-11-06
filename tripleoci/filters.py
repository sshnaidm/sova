import datetime

import tripleoci.config as config


class Filter(object):
    """Class for filtering jobs to remain only requested."""
    def __init__(self,
                 data,
                 days=None,
                 dates=None,
                 limit=None,
                 short=None,
                 fail=True,
                 exclude=None,
                 job_type=None,
                 periodic=False,
                 pipeline=None):
        """Filter class

            Receives a lot of filtering arguments:

        :param data: job data (Job class object)
        :param days: how many days to take, i.e. 7 - last week
        :param dates: specific dates in format ["%m-%d", ..]:['04-15', '05-02']
        :param limit: limit overall amount of jobs to analyze
        :param short: analyze only this type of jobs,
                        accepts short name: "ha","upgrades","nonha"
        :param fail: whether analyze and print only failed jobs
                        (true by default)
        :param exclude: exclude specific job type, i.e.
                        "gate-tripleo-ci-f22-containers"
        :param job_type: include only this job type (like short, but accepts
                         full name): "gate-tripleo-ci-f22-nonha"
        :param periodic: if it's periodic job (periodic=True) or patch (False)
        """
        self.data = sorted(data, key=lambda i: i.ts, reverse=True)
        self.default = [self.f_only_tracked] if not periodic else []
        self.limit = limit
        self.filters = [
            (self.f_days, days),
            (self.f_short, short),
            (self.f_fail, fail),
            (self.f_exclude, exclude),
            (self.f_dates, dates),
            (self.f_jobtype, job_type),
            (self.f_pipeline, pipeline),
        ]

    def run(self):
        """Combine filters

            It contains a chain of filters.
            default - leave only tracked jobs (TRACKED_JOBS in config.py)
                        but it's not relevant in periodic jobs
        :return: list of filtered jobs
        """
        if self.default:
            for fil in self.default:
                self.data = [job for job in self.data if fil(job)]
        for filt in self.filters:
            self.data = [job for job in self.data if filt[0](job, filt[1])]
        if self.limit:
            return list(self.data)[:self.limit]
        else:
            return list(self.data)

    def f_only_tracked(self, job):
        return job.name in config.PLUGIN_JOBS

    def _day_format(self, x):
        return datetime.date.strftime(x, "%m-%d")

    def _job_day_format(self, x):
        return datetime.date.strftime(x, "%m-%d")

    def f_days(self, job, days):
        if not days:
            return True
        today = datetime.date.today()
        dates = []
        for i in range(days):
            dates.append(self._day_format(today - datetime.timedelta(days=i)))
        job_date = self._job_day_format(job.ts)
        return job_date in dates

    def f_dates(self, job, dates):
        if not dates:
            return True
        job_date = self._job_day_format(job.ts)
        return job_date in dates

    def f_short(self, job, short):
        def shorten(x):
            return {'gate-tripleo-ci-f22-upgrades': 'upgrades',
                    'gate-tripleo-ci-f22-nonha': 'nonha',
                    'gate-tripleo-ci-f22-ha': 'ha',
                    'gate-tripleo-ci-f22-containers': 'containers',
                    'periodic-tripleo-ci-f22-ha-liberty': 'ha',
                    'periodic-tripleo-ci-f22-ha-mitaka': 'ha',
                    'periodic-tripleo-ci-f22-ha': 'ha',
                    'periodic-tripleo-ci-f22-nonha': 'nonha',
                    'periodic-tripleo-ci-f22-upgrades': 'upgrades',
                    }.get(x, x)

        if not short:
            return True
        return shorten(job.name) == short

    def f_fail(self, job, fail):
        return True if not fail else job.fail

    def f_pipeline(self, job, pipeline):
        if pipeline is None: return True
        return True if pipeline and job.pipeline == pipeline else False

    def f_exclude(self, job, exclude):
        return True if not exclude else job.name != exclude

    def f_jobtype(self, job, job_type):
        return True if not job_type else job.name == job_type
