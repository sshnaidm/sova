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
INDEX_HTML = os.path.join(DOWNLOAD_PATH, "index-gates.html")
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
        "tripleo-ci-centos-7-ovb-ha-oooq",
        "tripleo-ci-centos-7-ovb-ha-oooq-ipv6",
        'tripleo-ci-centos-7-ovb-ha-oooq-pike',
        "tripleo-ci-centos-7-ovb-ha-oooq-ocata",
        "tripleo-ci-centos-7-ovb-ha-oooq-newton",
        "tripleo-ci-centos-7-ovb-containers-oooq",
        "tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024",
        'tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet-pike',
        'tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet-ocata',
        ("tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024-puppet"
         "-newton"),
        "tripleo-ci-centos-7-ovb-fakeha-caserver",
        "tripleo-ci-centos-7-ovb-ha-tempest-oooq",
        "tripleo-ci-centos-7-ovb-convergence-oooq",

    ],
    "Scenarios": [
        "tripleo-ci-centos-7-scenario001-multinode-oooq",
        "tripleo-ci-centos-7-scenario002-multinode-oooq",
        "tripleo-ci-centos-7-scenario003-multinode-oooq",
        "tripleo-ci-centos-7-scenario004-multinode-oooq",
        "tripleo-ci-centos-7-scenario005-multinode-oooq",
        "tripleo-ci-centos-7-scenario006-multinode-oooq",
        'tripleo-ci-centos-7-scenario007-multinode-oooq',
        'tripleo-ci-centos-7-scenario008-multinode-oooq',
        'tripleo-ci-centos-7-scenario009-multinode-oooq',
    ],
    "Containers": [
        "tripleo-ci-centos-7-containers-multinode",
        "tripleo-ci-centos-7-scenario001-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario002-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario003-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario004-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario007-multinode-oooq-container",
    ],
    "Upgrades": [
        "tripleo-ci-centos-7-scenario001-multinode-upgrades",
        "tripleo-ci-centos-7-scenario002-multinode-upgrades",
        "tripleo-ci-centos-7-scenario003-multinode-upgrades",
        "tripleo-ci-centos-7-multinode-upgrades",
        "tripleo-ci-centos-7-containers-multinode-upgrades",
    ],
    "Multinode": [
        "tripleo-ci-centos-7-nonha-multinode-oooq",
        "tripleo-ci-centos-7-3nodes-multinode"
    ],
    "Undercloud": [
        "tripleo-ci-centos-7-undercloud-oooq",
        "tripleo-ci-centos-7-undercloud-containers",
    ],
    "Puppet": [
        "puppet-openstack-unit-4.8-centos-7",
        "puppet-openstack-lint",
        "puppet-openstack-syntax-4",
        "puppet-tripleo-puppet-unit-4.8-centos-7",
    ],
    "Images": [
        "tripleo-buildimage-overcloud-full-centos-7",
        "tripleo-buildimage-ironic-python-agent-centos-7",
        "tripleo-buildimage-overcloud-hardened-full-centos-7"
    ]

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
    console_name = 'job-output.txt.gz'

ACTIVE_PLUGIN_CONFIG = PLUGIN_TRIPLEOCI_CONFIG
