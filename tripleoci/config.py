import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('watchcat')
log.setLevel(logging.DEBUG)

DIR = os.path.dirname(os.path.realpath(__file__))
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
    '^openstack/puppet-.*'
)

PERIODIC_LOGS_URL = 'http://logs.openstack.org/periodic'
PERIODIC_URLS = [
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-mitaka',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-tempest',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-nonha',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-updates',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-fakeha-caserver',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-newton',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-ocata',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq',
    PERIODIC_LOGS_URL + 'periodic-tripleo-ci-centos-7-scenario001-multinode',
    PERIODIC_LOGS_URL + 'periodic-tripleo-ci-centos-7-scenario002-multinode',
    PERIODIC_LOGS_URL + 'periodic-tripleo-ci-centos-7-scenario003-multinode',
    PERIODIC_LOGS_URL + 'periodic-tripleo-ci-centos-7-scenario004-multinode',
]

DOWNLOAD_PATH = os.environ.get('OPENSHIFT_DATA_DIR',
                               os.path.join(os.environ["HOME"], "ci_status"))
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)
TMP_DIR = os.environ.get('OPENSHIFT_TMP_DIR', "/tmp/")
if os.path.exists(os.path.join(DIR, "..", "robi_id_rsa")):
    SSH_PRIV_KEY = os.path.join(DIR, "..", "robi_id_rsa")
elif os.path.exists(os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', "./"),
                                 "robi_id_rsa")):
    SSH_PRIV_KEY = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', "./"),
                                "robi_id_rsa")
else:
    SSH_PRIV_KEY = None
INDEX_HTML = os.path.join(DOWNLOAD_PATH, "index.html")
SSH_TIMEOUT = 120
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/mitaka", "stable/newton", "stable/ocata")
TRACKED_JOBS = (
    "gate-tripleo-ci-centos-7-ovb-nonha-mitaka",
    "gate-tripleo-ci-centos-7-ovb-ha-mitaka",
    "gate-tripleo-ci-centos-7-ovb-nonha-newton",
    "gate-tripleo-ci-centos-7-ovb-ha-newton",
    "gate-tripleo-ci-centos-7-ovb-nonha-ocata",
    "gate-tripleo-ci-centos-7-ovb-ha-ocata",
    "gate-tripleo-ci-centos-7-ovb-ha",
    "gate-tripleo-ci-centos-7-ovb-nonha",

    "gate-tripleo-ci-centos-7-ovb-ha-tempest",
    "gate-tripleo-ci-centos-7-ovb-ha-ipv6",
    "gate-tripleo-ci-centos-7-ovb-ha-oooq-nv",
    "gate-tripleo-ci-centos-7-ovb-nonha-oooq-nv",
    "gate-tripleo-ci-centos-7-ovb-containers-oooq-nv",
    "gate-tripleo-ci-centos-7-ovb-containers-oooq",
    "gate-tripleo-ci-centos-7-ovb-updates-nv",

    "gate-tripleo-ci-centos-7-nonha-multinode",
    "gate-tripleo-ci-centos-7-scenario001-multinode",
    "gate-tripleo-ci-centos-7-scenario002-multinode",
    "gate-tripleo-ci-centos-7-scenario003-multinode",
    "gate-tripleo-ci-centos-7-scenario004-multinode",
    "gate-tripleo-ci-centos-7-nonha-multinode-updates-nv",
    "gate-tripleo-ci-centos-7-multinode-upgrades-nv",

    "gate-tripleo-ci-centos-7-nonha-multinode-oooq",
    "gate-tripleo-ci-centos-7-undercloud-oooq",
    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario003-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario004-multinode-oooq",
    "gate-tripleo-ci-centos-7-scenario005-multinode-oooq",

    "gate-tripleo-ci-centos-7-undercloud",
    "gate-tripleo-ci-centos-7-undercloud-upgrades-nv",
    "gate-tripleo-ci-centos-7-undercloud-containers"
)
