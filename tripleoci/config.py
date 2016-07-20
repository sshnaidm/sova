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

PERIODIC_URLS = [
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-upgrades',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ha',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-nonha',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ha-liberty',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ha-mitaka',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ha-tempest',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-ha-liberty',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-ha-mitaka',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-ha-tempest',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-ha',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-nonha',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-centos-7-ovb-upgrades',
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
GERRIT_BRANCHES = ("master", "stable/liberty", "stable/mitaka")
TRACKED_JOBS = (
    "gate-tripleo-ci-centos-7-ha",
    "gate-tripleo-ci-centos-7-nonha",
    "gate-tripleo-ci-centos-7-upgrades",
    "gate-tripleo-ci-centos-7-ha-tempest",
    "gate-tripleo-ci-centos-7-nonha-liberty",
    "gate-tripleo-ci-centos-7-ha-liberty",
    "gate-tripleo-ci-centos-7-nonha-mitaka",
    "gate-tripleo-ci-centos-7-ha-mitaka",
    "gate-tripleo-ci-centos-7-ovb-ha",
    "gate-tripleo-ci-centos-7-ovb-nonha",
    "gate-tripleo-ci-centos-7-ovb-ha-tempest",
    "gate-tripleo-ci-centos-7-ovb-ha-liberty",
    "gate-tripleo-ci-centos-7-ovb-ha-mitaka",
)
