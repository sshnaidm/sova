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
    'openstack/tripleo-ansible',
    '^openstack/puppet-.*',
    # Non-TripleO repositories
    # 'openstack/neutron',
    # 'openstack/paunch',
    # 'openstack/nova',
    # 'openstack/aodh',
    # 'openstack/barbican',
    # 'openstack/ceilometer',
    # 'openstack/congress',
    # 'openstack/ec2api',
    # 'openstack/gnocchi',
    # 'openstack/heat',
    # 'openstack/ironic',
    # 'openstack/keystone',
    # 'openstack/mistral',
    # 'openstack/osc-lib',
    # 'openstack/panko',
    # 'openstack/python-openstackclient',
    # 'openstack/python-neutronclient',
    # 'openstack/tacker',
    # 'openstack/zaqar',
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
GERRIT_BRANCHES = ("master", "stable/pike", "stable/rocky",
                   "stable/queens")
PERIODIC_DAYS = 14
GATE_DAYS = 8
CIRCLE = 3
COLUMNED_TRACKED_JOBS = {
    "Standalone": [
        "tripleo-ci-centos-7-standalone",
        "tripleo-ci-fedora-28-standalone",
        "tripleo-ci-centos-7-standalone-upgrade",
        "tripleo-ci-centos-7-standalone-os-tempest",
        "tripleo-ci-centos-7-scenario001-standalone",
        "tripleo-ci-centos-7-scenario002-standalone",
        "tripleo-ci-centos-7-scenario003-standalone",
        "tripleo-ci-centos-7-scenario004-standalone",
        "tripleo-ci-centos-7-scenario010-standalone",
    ],
    "Containers": [
        "tripleo-ci-centos-7-containers-multinode",
        "tripleo-ci-centos-7-scenario009-multinode-oooq-container",
        "tripleo-build-containers-centos-7-rocky",
        "tripleo-build-containers-centos-7-buildah",
        "tripleo-build-containers-centos-7",
        "tripleo-build-containers-centos-7-buildah-stein",
        "tripleo-build-containers-centos-7-stein",
    ],
    "Undercloud": [
        "tripleo-ci-centos-7-undercloud-oooq",
        "tripleo-ci-centos-7-undercloud-containers",
    ],
    "Puppet": [
        "puppet-neutron-tripleo-standalone",
        "puppet-nova-tripleo-standalone",
        "puppet-keystone-tripleo-standalone",
        "puppet-glance-tripleo-standalone",
        "puppet-cinder-tripleo-standalone",
    ],
    "Update/Upgrades": [
        "tripleo-ci-centos-7-scenario000-multinode-oooq-container-updates",
        "tripleo-ci-centos-7-containerized-undercloud-upgrades",
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
