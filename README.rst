====
CI jobs parsing tool
====

Overview
---------

This tools puprose is to scan current jobs in TripleO CI and report about their
failure reasons.
In addition it could be used for tracking infra issues, bugs, etc.

History
---------

There are two pages in TripleO CI now: http://tripleo.org/cistatus.html and
http://tripleo.org/cistatus-periodic.html (doesn't work now) which shows current
patch and periodic jobs and their status - failed or succeeded.

The scripts that compose these pages is in tripleo-ci repository:
https://github.com/openstack-infra/tripleo-ci/blob/master/scripts/tripleo-jobs-gerrit.py and
https://github.com/openstack-infra/tripleo-ci/blob/master/scripts/tripleo-jobs.py

First one is working right now when upstream Jenkins are not available (security issues),
the second will work when upstream Jenkins will be accessible again.

First script just go over all upstream Jenkinses and requests it for all tripleo
jobs (by names), then reads their status and shows on the page.
The second one connects to upstream gerrit by ssh and gets patches data from it.
It asks for patches from a few projects, which run tripleo jobs (but not all).
Periodic jobs are not tracked now, because they are not in gerrit, you can see
their logs in:

* http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-ha-liberty/
* http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-ha-mitaka/
* http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-ha/
* http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-nonha/
* http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-upgrades/

The flow of parsing tool
---------

This tool shall read the data about all Tripleo CI jobs and report the reasons
for failures if they are failed.
It could be run from outside by any external script (by importing meow dunction)
or running watchcat.py in command line (with appropriate parameters in it).

Firstly it connects to gerrit by ssh using a special user `robo` (ask sshnaidm for
its private SSH key) and gets patches for all configured project in config.py.

Gerrit connection is done in utils.py file. The patches amount is limited to 200
to avoid overloading. This gives us all data about the patches that are opened
now and run TripleO CI in them.

For periodic jobs it connects to links (see above) and just parses the HTML page
to get all periodic jobs info from it.

Then it parses gerrit data or HTML data in case of periodic jobs and create list
of all jobs we have with some jobs related data like its length, status, time, etc.
See periodic.py and patches.py files for additional info.

Then it passes a given filters (in filters.py) and remain only those jobs we want
to analyze.

The script analyzes all jobs (analysis.py) and returns data about them.
If script runs in console it prints the info to console, if it run by app.py
it creates index.html using Jinja template template.html. For CSS and JS it uses
bootstrap framework (http://getbootstrap.com)

The analysis
---------

The analysis is done by searching log file for specific patterns (patterns.py).

The pattern contains:

-   file that it should contain it
-   text or regular expression to search
-   resulting message if pattern was found
-   tag - if it's code issue, or infra, or anything else

The script downloads the mentioned in the pattern file (JobFile in utils.py) and
searches there for a text or regular expression.

Regexp pattern could catch particular text and display it in the message.

If pattern is found, the resulting message will be added to output. The output
could contain more than one message if more than one pattern was found.

The report
---------

The report in console will contain jobs date, reasons for failure if found,
link to logs.
The report in HTML page will contain much more info: patch links, commit messages,
length and time, project and branch, etc.
It will be also a little statistics about the tags - how many percents "infra"
issues and how many jobs has known reasons. (_TODO_)

Roadmap
---------

* Generate statistics for today, yesterday, last week
* Show statistics in the page
* Find acceptable limits for patches amount
* Add grids to pages to look pretty
* Find a hosting for the page (openshift could be as temporary solution)
* Add parallelization to get web pages and analyzing
* Where to keep SSH private key for Gerrit?
