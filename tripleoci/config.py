import logging
import os
from flask import Markup

logging.basicConfig(
    format=('%(asctime)s - %(name)s - %(levelname)s - '
            '%(module)s.%(funcName)s:%(lineno)d - %(message)s'))
log = logging.getLogger('watchcat')
log.setLevel(logging.DEBUG)

DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(DIR, '..', 'html'))
PATTERN_FILE = os.path.join(DIR, 'data', 'patterns.yml')
# https://github.com/openstack-infra/project-config/blob/master/
# gerritbot/channels.yaml
PROJECTS = (
    'openstack/tripleo-quickstart',
    'openstack/tripleo-quickstart-extras',
    'openstack/tripleo-heat-templates',
    'openstack/dib-utils',
    'openstack/diskimage-builder',
    'openstack/instack',
    'openstack/instack-undercloud',
    'openstack/os-apply-config',
    'openstack/os-cloud-config',
    'openstack/os-collect-config',
    'openstack/os-net-config',
    'openstack/os-refresh-config',
    'openstack/python-tripleoclient',
    'openstack-infra/tripleo-ci',
    'openstack/tripleo-common',
    'openstack/tripleo-image-elements',
    'openstack/tripleo-puppet-elements',
    'openstack/tripleo-docs',
    'openstack/tripleo-quickstart',
    'openstack/tripleo-specs',
    'openstack/tripleo-ui',
    'openstack/tripleo-upgrade',
    '^openstack/puppet-.*',
    # # Non-TripleO repositories
    # 'openstack/neutron',
    'openstack/paunch',
    # 'openstack/nova',
    'openstack/aodh',
    'openstack/barbican',
    'openstack/ceilometer',
    'openstack/congress',
    # 'openstack/ec2api',
    'openstack/gnocchi',
    'openstack/heat',
    'openstack/ironic',
    'openstack/keystone',
    'openstack/mistral',
    'openstack/osc-lib',
    'openstack/panko',
    'openstack/python-openstackclient',
    'openstack/python-neutronclient',
    'openstack/tacker',
    'openstack/zaqar',
)


PERIODIC_LOGS_URL = [
    ('https://review.rdoproject.org/zuul/api/'
     'builds?pipeline=openstack-periodic'),
    ('https://review.rdoproject.org/zuul/api/'
     'builds?pipeline=openstack-periodic-24hr'),
    ('https://review.rdoproject.org/zuul/api/'
     'builds?pipeline=openstack-periodic-master'),
    ('https://review.rdoproject.org/zuul/api/'
     'builds?pipeline=openstack-periodic-latest-released'),
]
PERIODIC_URLS = []

DOWNLOAD_PATH = os.environ.get('OPENSHIFT_DATA_DIR',
                               os.path.join(os.environ["HOME"], "ci_status"))
# For running in container
if os.access("/cidata", os.W_OK):
    DOWNLOAD_PATH = "/cidata"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)
TMP_DIR = os.environ.get('OPENSHIFT_TMP_DIR', "/tmp/")
if os.path.exists(os.path.join(DIR, "..", "robi_id_rsa")):
    SSH_PRIV_KEY = os.path.join(DIR, "..", "robi_id_rsa")
elif os.path.exists(os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', "./"),
                                 "robi_id_rsa")):
    SSH_PRIV_KEY = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', "./"),
                                "robi_id_rsa")
elif os.path.exists(os.path.join(DOWNLOAD_PATH, "robi_id_rsa")):
    SSH_PRIV_KEY = os.path.join(DOWNLOAD_PATH, "robi_id_rsa")
else:
    SSH_PRIV_KEY = None
INDEX_HTML = os.path.join(DOWNLOAD_PATH, "index.html")
SSH_TIMEOUT = 120
WEB_TIMEOUT = (6.05, 15)
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/pike",
                   "stable/queens", "stable/rocky", "stable/stein")
PERIODIC_DAYS = 14
PERIODIC_PAGES = 25
GATE_DAYS = 7
CIRCLE = 3

# A brief note about the column titles below...
#
# The bootstrap nav tab class swallows click events, so adding an onclick
# handler within the <a> tag
# allows for primary click to have expected behavior, while leaving the href=
# in place allows for
# right click (open in new tab/window) to also work.
#
# The Markup() class is part of flask that is the preferred way to annotate
# HTML to not be escaped
# http://flask.pocoo.org/docs/0.12/templating/#controlling-autoescaping
# http://flask.pocoo.org/docs/0.12/api/#flask.Markup

COLUMNED_TRACKED_JOBS = {
    Markup('''<a href="http://dashboards.rdoproject.org/master" onclick="window.location.href='http://dashboards.rdoproject.org/master'">Master-promotion</a>'''): [  # noqa
        'periodic-tripleo-centos-7-master-promote-consistent-to-tripleo-ci-testing',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset010-master',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset030-master',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset037-updates-master',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset002-master-upload',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset020-master',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset021-master',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-master',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset035-master',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039-master',
        'periodic-tripleo-ci-centos-7-singlenode-featureset027-master',
        'periodic-tripleo-ci-centos-7-singlenode-featureset050-upgrades-master',
        'periodic-tripleo-ci-centos-7-standalone-master',
        'periodic-tripleo-ci-centos-7-standalone-upgrade-master',
        'periodic-tripleo-ci-centos-7-standalone-full-tempest-master',
        'periodic-tripleo-ci-centos-7-scenario001-standalone-master',
        'periodic-tripleo-ci-centos-7-scenario002-standalone-master',
        'periodic-tripleo-ci-centos-7-scenario003-standalone-master',
        'periodic-tripleo-ci-centos-7-scenario004-standalone-master',
        'periodic-tripleo-ci-fedora-28-standalone-master',
        'periodic-tripleo-fedora-28-master-containers-build-push',
        'periodic-tripleo-centos-7-master-containers-build-push',
    ],
    Markup('''<a href="http://dashboards.rdoproject.org/stein" onclick="window.location.href='http://dashboards.rdoproject.org/stein'">Stein-promotion</a>'''): [  # noqa
        'periodic-tripleo-centos-7-stein-promote-consistent-to-tripleo-ci-testing',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset010-stein',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset030-stein',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset037-updates-stein',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset002-stein-upload',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset020-stein',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset021-stein',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-stein',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset035-stein',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039-stein',
        'periodic-tripleo-ci-centos-7-singlenode-featureset027-stein',
        'periodic-tripleo-ci-centos-7-singlenode-featureset050-upgrades-stein',
        'periodic-tripleo-ci-centos-7-standalone-stein',
        'periodic-tripleo-ci-centos-7-standalone-upgrade-stein',
        'periodic-tripleo-ci-centos-7-scenario001-standalone-stein',
        'periodic-tripleo-ci-centos-7-scenario002-standalone-stein',
        'periodic-tripleo-ci-centos-7-scenario003-standalone-stein',
        'periodic-tripleo-ci-centos-7-scenario004-standalone-stein',
        'periodic-tripleo-ci-fedora-28-standalone-stein',
        'periodic-tripleo-fedora-28-stein-containers-build-push',
        'periodic-tripleo-centos-7-stein-containers-build-push',
    ],
    Markup('''<a href="http://dashboards.rdoproject.org/rocky" onclick="window.location.href='http://dashboards.rdoproject.org/rocky'">Rocky-promotion</a>'''): [  # noqa
        'periodic-tripleo-centos-7-rocky-promote-consistent-to-tripleo-ci-testing',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset010-rocky',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-rocky',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-rocky',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-rocky',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-rocky',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset030-rocky',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset037-updates-rocky',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset002-rocky-upload',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset020-rocky',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset021-rocky',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-rocky',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset035-rocky',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039-rocky',
        'periodic-tripleo-ci-centos-7-singlenode-featureset027-rocky',
        'periodic-tripleo-ci-centos-7-singlenode-featureset050-upgrades-rocky',
        'periodic-tripleo-centos-7-rocky-containers-build-push'
    ],
    Markup('''<a href="http://dashboards.rdoproject.org/queens" onclick="window.location.href='http://dashboards.rdoproject.org/queens'">Queens-promotion</a>'''): [  # noqa
        'periodic-tripleo-centos-7-queens-containers-build',
        'periodic-tripleo-centos-7-queens-promote-consistent-to-tripleo-ci-testing',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset010-queens',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-queens',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-queens',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-queens',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-queens',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset030-queens',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset037-updates-queens',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset002-queens-upload',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset021-queens',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-queens',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset035-queens',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset020-queens',
    ],
    Markup('''<a href="http://dashboards.rdoproject.org/pike" onclick="window.location.href='http://dashboards.rdoproject.org/pike'">Pike-promotion</a>'''): [  # noqa
        'periodic-tripleo-centos-7-pike-containers-build',
        'periodic-tripleo-centos-7-pike-promote-consistent-to-tripleo-ci-testing',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset010-pike',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-pike',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-pike',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-pike',
        'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-pike',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-pike',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset002-pike-upload',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset021-pike',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset022-pike',
        'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-pike',
        'periodic-tripleo-ci-centos-7-ovb-1ctlr_2comp-featureset020-pike',
    ],
}

RDOCI = {
    'console': '/job-output.txt',
    "postci": '/logs/undercloud/var/log/extra/logstash.txt.gz',
    'ironic-conductor': '/logs/undercloud/var/log/ironic/ironic-conductor.txt.gz',
    'syslog': '/logs/undercloud/var/log/journal.txt.gz',
    'logstash': '/logs/undercloud/var/log/extra/logstash.txt.gz',
    'errors': '/logs/undercloud/var/log/extra/errors.txt.gz',
    'bmc': '/logs/bmc-console.log',

}

PLUGIN = RDOCI
TRACKED_JOBS = [k for i in COLUMNED_TRACKED_JOBS.values() for k in i]
PLUGIN_JOBS = TRACKED_JOBS


class PLUGIN_RDOCI_CONFIG:
    console_name = 'job-output.txt.gz'
    main_index_timeout = 1100


ACTIVE_PLUGIN_CONFIG = PLUGIN_RDOCI_CONFIG
