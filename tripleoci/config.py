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
GATE_DAYS = 8
CIRCLE = 3
COLUMNED_TRACKED_JOBS = {
    "OVB": [
        "legacy-tripleo-ci-centos-7-ovb-ha",
        "legacy-tripleo-ci-centos-7-ovb-nonha",
        "legacy-tripleo-ci-centos-7-ovb-ha-oooq",
        "legacy-tripleo-ci-centos-7-ovb-ha-oooq-ocata",
        "legacy-tripleo-ci-centos-7-ovb-ha-oooq-newton",
        "legacy-tripleo-ci-centos-7-ovb-containers-oooq",
        'legacy-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet-pike',
        'legacy-tripleo-ci-centos-7-ovb-ha-oooq-pike',
        "legacy-tripleo-ci-centos-7-ovb-fakeha-caserver",
        "legacy-tripleo-ci-centos-7-ovb-ha-tempest-oooq",
        "legacy-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024",
        "legacy-tripleo-ci-centos-7-ovb-convergence-oooq",
        ("legacy-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet"
         "-newton"),
        ("legacy-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet"
         "-ocata"),
    ],
    "Scenarios": [
        "legacy-tripleo-ci-centos-7-scenario001-multinode-oooq",
        "legacy-tripleo-ci-centos-7-scenario001-multinode-oooq-puppet",
        "legacy-tripleo-ci-centos-7-scenario002-multinode-oooq",
        "legacy-tripleo-ci-centos-7-scenario002-multinode-oooq-puppet",
        "legacy-tripleo-ci-centos-7-scenario003-multinode-oooq",
        "legacy-tripleo-ci-centos-7-scenario003-multinode-oooq-puppet",
        "legacy-tripleo-ci-centos-7-scenario004-multinode-oooq",
        "legacy-tripleo-ci-centos-7-scenario004-multinode-oooq-puppet",
        "legacy-tripleo-ci-centos-7-scenario005-multinode-oooq",
        'legacy-tripleo-ci-centos-7-scenario007-multinode-oooq',
        'legacy-tripleo-ci-centos-7-scenario007-multinode-oooq-puppet',
    ],
    "Containers": [
        "legacy-tripleo-ci-centos-7-containers-multinode",
        "legacy-tripleo-ci-centos-7-scenario001-multinode-oooq-container",
        "legacy-tripleo-ci-centos-7-scenario002-multinode-oooq-container",
        "legacy-tripleo-ci-centos-7-scenario003-multinode-oooq-container",
        "legacy-tripleo-ci-centos-7-scenario004-multinode-oooq-container",
    ],
    "Upgrades": [
        "legacy-tripleo-ci-centos-7-scenario001-multinode-upgrades",
        "legacy-tripleo-ci-centos-7-scenario002-multinode-upgrades",
        "legacy-tripleo-ci-centos-7-scenario003-multinode-upgrades",
        "legacy-tripleo-ci-centos-7-multinode-upgrades",
        "legacy-tripleo-ci-centos-7-containers-multinode-upgrades",
    ],
    "Multinode": [
        "legacy-tripleo-ci-centos-7-nonha-multinode-oooq",
    ],
    "Undercloud": [
        "legacy-tripleo-ci-centos-7-undercloud-oooq",
        "legacy-tripleo-ci-centos-7-undercloud-containers",
    ],

}
TRIPLEOCI = {
    'console': '/job-output.txt',
    'postci': '/logs/postci.txt',
    'ironic-conductor': '/logs/undercloud/var/log/ironic/ironic-conductor.txt',
    'syslog': '/logs/undercloud/var/log/messages',
    'logstash': '/logs/undercloud/var/log/extra/logstash.txt'
}

PLUGIN = TRIPLEOCI
TRACKED_JOBS = [k for i in COLUMNED_TRACKED_JOBS.values() for k in i]
PLUGIN_JOBS = TRACKED_JOBS


class PLUGIN_TRIPLEOCI_CONFIG(object):
    console_name = 'job-output.txt'

ACTIVE_PLUGIN_CONFIG = PLUGIN_TRIPLEOCI_CONFIG
