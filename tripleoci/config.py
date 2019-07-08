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
    'openstack/ansible-role-container-registry',
    'openstack/ansible-role-tripleo-modify-image',
    'openstack/dib-utils',
    'openstack/diskimage-builder',
    'openstack/openstack-ansible-os_tempest',
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
    'openstack/tripleo-ansible',
    'openstack/tripleo-upgrade',
    'openstack/tripleo-validations',
    'openstack/tripleo-repos',
    '^openstack/puppet-.*',
    # Non-TripleO repositories
    # 'openstack/neutron',
    'openstack/paunch',
    # 'openstack/nova',
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


PERIODIC_LOGS_URL = [
    ('https://review.rdoproject.org/zuul/api/'
     'builds?pipeline=openstack-periodic'),
    ('https://review.rdoproject.org/zuul/api/'
     'builds?pipeline=openstack-periodic-24hr'),
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
WEB_TIMEOUT = (3.05, 1)
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/pike",
                   "stable/queens", "stable/rocky", "stable/stein")
PERIODIC_DAYS = 14
PERIODIC_PAGES = 2
GATE_DAYS = 8
CIRCLE = 3
COLUMNED_TRACKED_JOBS = {
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
    "Standalone": [
        "tripleo-ci-centos-7-standalone",
        "tripleo-ci-fedora-28-standalone",
        "tripleo-ci-centos-7-scenario001-standalone",
        "tripleo-ci-centos-7-scenario002-standalone",
        "tripleo-ci-centos-7-scenario003-standalone",
        "tripleo-ci-centos-7-scenario004-standalone",
        "tripleo-ci-centos-7-scenario012-standalone",
        "tripleo-ci-centos-7-scenario010-standalone",
        "tripleo-ci-centos-7-standalone-os-tempest",
        "tripleo-ci-centos-7-standalone-rocky",
    ],
    "Containers": [
        "tripleo-ci-centos-7-containers-multinode",
        "tripleo-ci-centos-7-scenario001-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario002-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario002-multinode-oooq-container-refstack",
        "tripleo-ci-centos-7-scenario003-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario004-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario005-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario006-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario007-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario008-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario009-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario010-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario011-multinode-oooq-container",
        "tripleo-ci-centos-7-scenario012-multinode-oooq-container"
    ],
    "Multinode": [
        "tripleo-ci-centos-7-nonha-multinode-oooq",
        "tripleo-ci-centos-7-3nodes-multinode",
    ],
    "Undercloud": [
        "tripleo-ci-centos-7-undercloud-oooq",
        "tripleo-ci-centos-7-undercloud-containers",
    ],
    "Update/Upgrades": [
        "tripleo-ci-centos-7-scenario000-multinode-oooq-container-updates",
        "tripleo-ci-centos-7-containerized-undercloud-upgrades",
        "tripleo-ci-centos-7-undercloud-upgrades",
        "tripleo-ci-centos-7-scenario000-multinode-oooq-container-upgrades",
        "tripleo-ci-centos-7-standalone-upgrade-stein",
        "tripleo-ci-centos-7-standalone-upgrade",
    ],
    "Images": [
        "tripleo-buildimage-overcloud-full-centos-7",
        "tripleo-buildimage-ironic-python-agent-centos-7",
        "tripleo-buildimage-overcloud-hardened-full-centos-7",
        "tripleo-build-containers-centos-7",
        "tripleo-build-containers-centos-7-rocky",
        "tripleo-build-containers-centos-7-stein",
        "tripleo-build-containers-centos-7-buildah",
    ],
    "Branches": [
        "tripleo-ci-centos-7-containers-multinode-stein",
        "tripleo-ci-centos-7-containers-multinode-rocky",
        "tripleo-ci-centos-7-containers-multinode-queens",
        "tripleo-ci-centos-7-containers-multinode-pike",

    ],
    "OVB": [
        'tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024',
        'tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020-master',
        'tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset020',
        'tripleo-ci-centos-7-ovb-1ctlr_1comp-featureset022',
        ('tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039-'
         'master'),
        'tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001',
        ('tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-ocata-'
         'branch'),
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-pike-branch',
        ('tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-queens-'
         'branch'),
        ('tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-rocky-'
         'branch'),
        ('tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-stein-'
         'branch'),
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset021',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset035',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset042',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset053',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-master-vexxhost',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-stein-vexxhost',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-rocky-vexxhost',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp_1supp-featureset039-ovb-master',
        'tripleo-ci-centos-7-ovb-3ctlr_1comp-featureset001-ovb-master',
    ],
    "RDO cloud multinode": [
        'tripleo-ci-centos-7-multinode-1ctlr-featureset010',
    ],
    "RDO cloud upgrades": [
        'tripleo-ci-centos-7-container-to-container-featureset051-upgrades',
        'tripleo-ci-centos-7-container-to-container-upgrades-master',
        'tripleo-ci-centos-7-container-to-container-upgrades-queens',
    ]
}
TRIPLEOCI = {
    'console': '/job-output.txt',
    "postci": '/logs/undercloud/var/log/extra/logstash.txt.gz',
    'ironic-conductor': ('/logs/undercloud/var/log/ironic/ironic-conductor.'
                         'txt.gz'),
    'syslog': '/logs/undercloud/var/log/journal.txt.gz',
    'logstash': '/logs/undercloud/var/log/extra/logstash.txt.gz',
    'errors': '/logs/undercloud/var/log/extra/errors.txt.gz',
    'bmc': '/logs/bmc-console.log',

}

PLUGIN = TRIPLEOCI
TRACKED_JOBS = [k for i in COLUMNED_TRACKED_JOBS.values() for k in i]
PLUGIN_JOBS = TRACKED_JOBS


class PLUGIN_TRIPLEOCI_CONFIG(object):
    console_name = 'job-output.txt.gz'


ACTIVE_PLUGIN_CONFIG = PLUGIN_TRIPLEOCI_CONFIG
