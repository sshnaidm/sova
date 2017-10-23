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
WEB_TIMEOUT = (3.05, 1)
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/newton", "stable/ocata", "stable/pike")
PERIODIC_DAYS = 14
GATE_DAYS = 7
CIRCLE = 3

PERIODIC_4H = 'https://logs.rdoproject.org/openstack-periodic-4hr/'
PERIODIC_24H = 'https://logs.rdoproject.org/openstack-periodic-24hr/'


#PERIODIC_4H + 'periodic-tripleo-centos-7-master-containers-build',
#PERIODIC_4H + 'periodic-tripleo-centos-7-master-images-build',
#PERIODIC_4H + 'periodic-tripleo-centos-7-master-promote-consistent-to-tripleo-ci-testing',
#PERIODIC_24H + 'periodic-tripleo-centos-7-newton-promote-consistent-to-tripleo-ci-testing',
#PERIODIC_24H + 'periodic-tripleo-centos-7-ocata-promote-consistent-to-tripleo-ci-testing',
#PERIODIC_4H + 'periodic-tripleo-centos-7-pike-containers-build',
#PERIODIC_4H + 'periodic-tripleo-centos-7-pike-images-build',
#PERIODIC_4H + 'periodic-tripleo-centos-7-pike-promote-consistent-to-tripleo-ci-testing',

COLUMNED_TRACKED_JOBS = {
    "Master-promotion": [
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset005-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset006-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset007-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset008-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-master',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-master-upload',
],
    'Pike-promotion':[
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset005-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset006-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset007-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset008-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset016-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset017-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset018-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-multinode-1ctlr-featureset019-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-pike',
        PERIODIC_4H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-pike-upload',

    ],
    'Ocata-promotion':[
        PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-ocata',
        PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-ocata',
        PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-ocata-upload',

    ],
    "Newton-promotion": [
        PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-newton',
        PERIODIC_24H + 'periodic-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset002-newton-upload',

    ],
    "RDO cloud OVB": [
        "gate-tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-master-nv",
        "gate-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-master-nv",
        "gate-tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset022-master-nv"
    ],
    "RDO cloud upgrades": [
        "gate-tripleo-ci-centos-7-containers-multinode-upgrades-master",
        "gate-tripleo-ci-centos-7-containers-multinode-upgrades-pike",
        "gate-tripleo-ci-centos-7-multinode-upgrades-master",
        "gate-tripleo-ci-centos-7-multinode-upgrades-pike",
        "gate-tripleo-ci-centos-7-multinode-upgrades-ocata",
        "gate-tripleo-ci-centos-7-undercloud-upgrades-master",
        "gate-tripleo-ci-centos-7-undercloud-upgrades-pike",
        "gate-tripleo-ci-centos-7-undercloud-upgrades-ocata",
        "gate-tripleo-ci-centos-7-multinode-1ctlr-featureset012-upgrades-master",
        "gate-tripleo-ci-centos-7-multinode-1ctlr-featureset012-upgrades-pike",
        "gate-tripleo-ci-centos-7-multinode-1ctlr-featureset014-upgrades-master",
        "gate-tripleo-ci-centos-7-multinode-1ctlr-featureset014-upgrades-pike",
    ]
}

RDOCI = {
    'console': '/console.txt',
    "postci": '/undercloud/var/log/extra/logstash.txt.gz',
    'ironic-conductor': '/undercloud/var/log/ironic/ironic-conductor.txt.gz',
    'syslog': '/undercloud/var/log/message.gz',
    'logstash': '/undercloud/var/log/extra/logstash.txt.gz'

}

PLUGIN = RDOCI
TRACKED_JOBS = [k for i in COLUMNED_TRACKED_JOBS.values() for k in i]
PLUGIN_JOBS = TRACKED_JOBS


class PLUGIN_RDOCI_CONFIG:
    console_name = 'console.txt.gz'
    main_index_timeout = 1100

ACTIVE_PLUGIN_CONFIG = PLUGIN_RDOCI_CONFIG
