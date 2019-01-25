import logging
import os

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
    'openstack/tripleo-incubator',
    'openstack/tripleo-puppet-elements',
    'openstack/tripleo-docs',
    'openstack/tripleo-quickstart',
    'openstack/tripleo-specs',
    'openstack/tripleo-ui',
    '^openstack/puppet-.*',
    # Non-TripleO repositories
    'openstack/neutron',
    'openstack/nova',
    'openstack/aodh',
    'openstack/barbican',
    'openstack/ceilometer',
    'openstack/congress',
    'openstack/ec2api',
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

PERIODIC_LOGS_URL = 'http://logs.openstack.org/periodic'
PERIODIC_URLS = [
    PERIODIC_LOGS_URL + ('/periodic-tripleo-ci-centos-7-'
                         'ovb-1ctlr_1comp_1ceph-featureset024'),
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-fakeha-caserver',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-oooq',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-pike-oooq',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-ocata-oooq',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-newton-oooq',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-nonha-containers',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-ocata',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-pike',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-master',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-scenario001-multinode-oooq',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-scenario002-multinode-oooq',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-scenario003-multinode-oooq',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-scenario004-multinode-oooq',
]

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
WEB_TIMEOUT = (3.05, 1)
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/newton", "stable/ocata", "stable/pike")
PERIODIC_DAYS = 14
GATE_DAYS = 14
CIRCLE = 3
TRACKED_JOBS = (
    "gate-tripleo-ci-centos-7-ovb-ha",
    "gate-tripleo-ci-centos-7-ovb-nonha",

    "gate-tripleo-ci-centos-7-ovb-ha-oooq",
    "gate-tripleo-ci-centos-7-ovb-ha-oooq-ocata",
    "gate-tripleo-ci-centos-7-ovb-ha-oooq-newton",
    "gate-tripleo-ci-centos-7-ovb-containers-oooq",
    'gate-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet-pike',
    'gate-tripleo-ci-centos-7-ovb-ha-oooq-pike',

    "gate-tripleo-ci-centos-7-nonha-multinode-oooq",
    "gate-tripleo-ci-centos-7-nonha-multinode-oooq-nv",
    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario003-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario004-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario005-multinode-oooq",

    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq-puppet",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq-puppet",
    "gate-tripleo-ci-centos-7-scenario003-multinode-oooq-puppet",
    "gate-tripleo-ci-centos-7-scenario004-multinode-oooq-puppet",
    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq-puppet-nv",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq-puppet-nv",

    "gate-tripleo-ci-centos-7-scenario001-multinode-upgrades",
    "gate-tripleo-ci-centos-7-scenario002-multinode-upgrades",
    "gate-tripleo-ci-centos-7-scenario003-multinode-upgrades",

    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq-container",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq-container",
    "gate-tripleo-ci-centos-7-scenario003-multinode-oooq-container",
    "gate-tripleo-ci-centos-7-scenario004-multinode-oooq-container",

    ("gate-tripleo-ci-centos-7-scenario001-"
     "multinode-oooq-container-upgrades-nv"),
    ("gate-tripleo-ci-centos-7-scenario002-"
     "multinode-oooq-container-upgrades-nv"),
    ("gate-tripleo-ci-centos-7-scenario003-"
     "multinode-oooq-container-upgrades-nv"),
    ("gate-tripleo-ci-centos-7-scenario004-"
     "multinode-oooq-container-upgrades-nv"),

    "gate-tripleo-ci-centos-7-containers-multinode",
    "gate-tripleo-ci-centos-7-nonha-multinode-updates-nv",
    "gate-tripleo-ci-centos-7-3nodes-multinode-nv",
    "gate-tripleo-ci-centos-7-multinode-upgrades-nv",
    "gate-tripleo-ci-centos-7-multinode-upgrades",
    "gate-tripleo-ci-centos-7-containers-multinode-upgrades-nv",
    "gate-tripleo-ci-centos-7-containers-multinode-upgrades",

    "gate-tripleo-ci-centos-7-undercloud-oooq",
    "gate-tripleo-ci-centos-7-undercloud-upgrades-nv",
    "gate-tripleo-ci-centos-7-undercloud-containers",

    "gate-tripleo-ci-centos-7-ovb-fakeha-caserver",
    "gate-tripleo-ci-centos-7-ovb-ha-tempest-oooq",

    "gate-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024",
    "gate-tripleo-ci-centos-7-ovb-convergence-oooq",
    ("gate-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet"
     "-newton"),
     ("gate-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet"
      "-ocata"),
    'gate-tripleo-ci-centos-7-scenario005-multinode-oooq-nv',
    'gate-tripleo-ci-centos-7-scenario006-multinode-oooq-nv',
    'gate-tripleo-ci-centos-7-scenario007-multinode-oooq',
    'gate-tripleo-ci-centos-7-scenario007-multinode-oooq-puppet',
    'gate-tripleo-ci-centos-7-scenario007-multinode-oooq-puppet-nv',
    'gate-tripleo-ci-centos-7-scenario008-multinode-oooq-nv',
)

PERIODIC_4H = 'https://logs.rdoproject.org/openstack-periodic-4hr/'
PERIODIC_24H = 'https://logs.rdoproject.org/openstack-periodic-24hr/'

RDOCI_JOBS = (
    #PERIODIC_4H + 'periodic-tripleo-centos-7-master-containers-build',
    #PERIODIC_4H + 'periodic-tripleo-centos-7-master-images-build',
    #PERIODIC_4H + 'periodic-tripleo-centos-7-master-promote-consistent-to-tripleo-ci-testing',
    #PERIODIC_24H + 'periodic-tripleo-centos-7-newton-promote-consistent-to-tripleo-ci-testing',
    #PERIODIC_24H + 'periodic-tripleo-centos-7-ocata-promote-consistent-to-tripleo-ci-testing',
    #PERIODIC_4H + 'periodic-tripleo-centos-7-pike-containers-build',
    #PERIODIC_4H + 'periodic-tripleo-centos-7-pike-images-build',
    #PERIODIC_4H + 'periodic-tripleo-centos-7-pike-promote-consistent-to-tripleo-ci-testing',


    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset005',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset005-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset005-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset006',

    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset006-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset006-pike',

    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset007',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset007-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset007-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset008',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset008-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset008-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-master',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-ocata',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-master-upload',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-master-uploader',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-newton',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-newton-upload',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-newton-uploader',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-ocata',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-ocata-upload',
    PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-ocata-uploader',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-pike',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-pike-upload',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-pike-uploader',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-scenario001-standalone-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-scenario002-standalone-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-scenario003-standalone-master',
    PERIODIC_4H + 'periodic-tripleo-ci-centos-7-scenario004-standalone-master',
)
TRIPLEOCI = {
    'console': '/console.html',
    'postci': '/logs/postci.txt',
    'ironic-conductor': '/logs/undercloud/var/log/ironic/ironic-conductor.txt',
    'syslog': '/logs/undercloud/var/log/messages',
    'logstash': '/logs/undercloud/var/log/extra/logstash.txt'
}

RDOCI = {
    'console': '/console.html',
    "postci": '/undercloud/var/log/extra/logstash.txt',
    'ironic-conductor': '/undercloud/var/log/ironic/ironic-conductor.txt',
    'syslog': '/undercloud/var/log/messages',
    'logstash': '/undercloud/var/log/extra/logstash.txt'

}

PLUGIN = RDOCI
PLUGIN_JOBS = RDOCI_JOBS


class PLUGIN_RDOCI_CONFIG:
    console_name = 'console.html'
    main_index_timeout = 1100


class PLUGIN_TRIPLEOCI_CONFIG:
    console_name = 'console.html'

ACTIVE_PLUGIN_CONFIG = PLUGIN_RDOCI_CONFIG
COLUMNS = [
    {'Master': 'master'},
]
COLUMNS += [{
    i.replace('stable/', '').capitalize(): i.replace('stable/', '')}
    for i in GERRIT_BRANCHES if "stable" in i]
