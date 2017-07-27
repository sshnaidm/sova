import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s')
log = logging.getLogger('watchcat')
log.setLevel(logging.DEBUG)

DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(DIR, '..', 'html'))
PATTERN_FILE = os.path.join(DIR, 'data', 'patterns.yml')
# https://github.com/openstack-infra/project-config/blob/master/
# gerritbot/channels.yaml
PROJECTS = (
    # 'openstack/tripleo-quickstart',
    # 'openstack/tripleo-quickstart-extras',
    # 'openstack/tripleo-heat-templates',
    # 'openstack/dib-utils',
    # 'openstack/diskimage-builder',
    # 'openstack/instack',
    # 'openstack/instack-undercloud',
    # 'openstack/os-apply-config',
    # 'openstack/os-cloud-config',
    # 'openstack/os-collect-config',
    # 'openstack/os-net-config',
    # 'openstack/os-refresh-config',
    # 'openstack/python-tripleoclient',
    'openstack-infra/tripleo-ci',
    # 'openstack/tripleo-common',
    # 'openstack/tripleo-image-elements',
    # 'openstack/tripleo-incubator',
    # 'openstack/tripleo-puppet-elements',
    # 'openstack/tripleo-docs',
    # 'openstack/tripleo-quickstart',
    # 'openstack/tripleo-specs',
    # 'openstack/tripleo-ui',
    # '^openstack/puppet-.*',
    # # Non-TripleO repositories
    # 'openstack/neutron',
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
PERIODIC_URLS = [
    PERIODIC_LOGS_URL + ('/periodic-tripleo-ci-centos-7-'
                         'ovb-1ctlr_1comp_1ceph-featureset024'),
    # PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-fakeha-caserver',
    # PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-oooq',
    # PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-ocata-oooq',
    # PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-newton-oooq',
    # PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-nonha-containers',
    # PERIODIC_LOGS_URL +
    # '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-ocata',
    # PERIODIC_LOGS_URL +
    # '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-master',
    # PERIODIC_LOGS_URL +
    # '/periodic-tripleo-ci-centos-7-scenario001-multinode-oooq',
    # PERIODIC_LOGS_URL +
    # '/periodic-tripleo-ci-centos-7-scenario002-multinode-oooq',
    # PERIODIC_LOGS_URL +
    # '/periodic-tripleo-ci-centos-7-scenario003-multinode-oooq',
    # PERIODIC_LOGS_URL +
    # '/periodic-tripleo-ci-centos-7-scenario004-multinode-oooq',
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
TRACKED_JOBS = (
    "gate-tripleo-ci-centos-7-ovb-ha",
    "gate-tripleo-ci-centos-7-ovb-nonha",
    "gate-tripleo-ci-centos-7-ovb-updates",

    "gate-tripleo-ci-centos-7-ovb-ha-oooq",
    "gate-tripleo-ci-centos-7-ovb-ha-oooq-ocata",
    "gate-tripleo-ci-centos-7-ovb-ha-oooq-newton",
    "gate-tripleo-ci-centos-7-ovb-containers-oooq-nv",
    "gate-tripleo-ci-centos-7-ovb-containers-oooq",

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
    "gate-tripleo-ci-centos-7-scenario005-multinode-oooq-puppet",
    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq-puppet-nv",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq-puppet-nv",

    "gate-tripleo-ci-centos-7-scenario001-multinode-upgrades-nv",
    "gate-tripleo-ci-centos-7-scenario002-multinode-upgrades-nv",
    "gate-tripleo-ci-centos-7-scenario003-multinode-upgrades-nv",
    "gate-tripleo-ci-centos-7-scenario004-multinode-upgrades-nv",

    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq-container",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq-container",
    "gate-tripleo-ci-centos-7-scenario003-multinode-oooq-container",
    "gate-tripleo-ci-centos-7-scenario004-multinode-oooq-container",

    "gate-tripleo-ci-centos-7-scenario001-multinode-oooq-container-upgrades",
    "gate-tripleo-ci-centos-7-scenario002-multinode-oooq-container-upgrades",
    "gate-tripleo-ci-centos-7-scenario003-multinode-oooq-container-upgrades",
    "gate-tripleo-ci-centos-7-scenario004-multinode-oooq-container-upgrades",

    "gate-tripleo-ci-centos-7-containers-multinode-nv",
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
    "gate-tripleo-ci-centos-7-undercloud-containers-nv",

    "gate-tripleo-ci-centos-7-ovb-fakeha-caserver",
    "gate-tripleo-ci-centos-7-ovb-ha-tempest-oooq",

    "gate-tripleo-ci-centos-7-ovb-1ctlr_1comp_1ceph-featureset024"
)
RDOCI_JOBS = (
    'rdo-delorean-promote-newton',
    'rdo-promote-build-images-master',
    'rdo-promote-get-hash-master',
    'rdo-promote-get-hash-master-current-tripleo',
    'rdo-promote-get-hash-ocata-current-triple',
    'rdo_trunk-promote-master-current-tripleo',
    'rdo_trunk-promote-ocata-current-tripleo',
    'tqe-containers-gate-master-tripleo-ci-delorean-full-containers_minimal',
    'tripleo-dlrn-promote',
    'tripleo-dlrn-promote-ocata',
    'tripleo-quickstart-extras-gate-master-tripleo-ci-delorean-full-minimal_pacemaker',
    'tripleo-quickstart-extras-gate-newton-delorean-full-minimal',
    'tripleo-quickstart-gate-master-delorean-full-minimal',
    'tripleo-quickstart-gate-master-delorean-quick-basic',
    'tripleo-quickstart-gate-master-full-images',
    'tripleo-quickstart-gate-master-tripleo-ci-delorean-full-minimal',
    'tripleo-quickstart-gate-newton-delorean-full-minimal_pacemaker',
    'tripleo-quickstart-gate-newton-delorean-quick-basic',
    'tripleo-quickstart-gate-ocata-delorean-full-minimal',
    'tripleo-quickstart-gate-ocata-delorean-quick-basic',
    'tripleo-quickstart-gate-ocata-full-images',
    'tripleo-quickstart-periodic-full-tempest-master-delorean-full-deploy-minimal_pacemaker',
    'tripleo-quickstart-periodic-master-delorean-devmode_tempest-minimal',
    'tripleo-quickstart-periodic-master-delorean-feature-scale-deploy-scale_compute',
    'tripleo-quickstart-periodic-master-delorean-full-deploy-minimal',
    'tripleo-quickstart-periodic-master-delorean-full-deploy-minimal_pacemaker',
    'tripleo-quickstart-periodic-master-delorean-images-minimal',
    'tripleo-quickstart-periodic-master-delorean-images-minimal_pacemaker',
    'tripleo-quickstart-periodic-newton-delorean-feature-scale-deploy-scale_compute',
    'tripleo-quickstart-periodic-newton-delorean-full-deploy-minimal',
    'tripleo-quickstart-periodic-newton-delorean-full-deploy-minimal_pacemaker',
    'tripleo-quickstart-periodic-newton-delorean-images-minimal',
    'tripleo-quickstart-periodic-newton-delorean-images-minimal_pacemaker',
    'tripleo-quickstart-periodic-newton-delorean-ooo-snap-minimal',
    'tripleo-quickstart-promote-master-build-images',
    'tripleo-quickstart-promote-master-current-tripleo-delorean-minimal',
    'tripleo-quickstart-promote-master-current-tripleo-delorean-minimal_pacemaker',
    'tripleo-quickstart-promote-master-delorean-minimal',
    'tripleo-quickstart-promote-master-delorean-minimal_pacemaker',
    'tripleo-quickstart-promote-newton-cloudsig-stable-build-images',
    'tripleo-quickstart-promote-newton-cloudsig-stable-minimal',
    'tripleo-quickstart-promote-newton-cloudsig-stable-minimal_pacemaker',
    'tripleo-quickstart-promote-newton-cloudsig-testing-build-images',
    'tripleo-quickstart-promote-newton-cloudsig-testing-minimal',
    'tripleo-quickstart-promote-newton-cloudsig-testing-minimal_pacemaker',
    'tripleo-quickstart-promote-newton-delorean-build-images',
    'tripleo-quickstart-promote-newton-delorean-minimal',
    'tripleo-quickstart-promote-newton-delorean-minimal_pacemaker',
    'tripleo-quickstart-promote-ocata-build-images',
    'tripleo-quickstart-promote-ocata-cloudsig-stable-build-images',
    'tripleo-quickstart-promote-ocata-cloudsig-stable-minimal_pacemaker',
    'tripleo-quickstart-promote-ocata-cloudsig-testing-build-images',
    'tripleo-quickstart-promote-ocata-cloudsig-testing-minimal',
    'tripleo-quickstart-promote-ocata-cloudsig-testing-minimal_pacemaker',
    'tripleo-quickstart-promote-ocata-rdo_trunk-minimal',
    'tripleo-quickstart-promote-ocata-rdo_trunk-minimal_pacemaker',
    'tripleo-quickstart-upgrade-major-mitaka-to-master',
    'weirdo-master-promote-packstack-scenario001',
    'weirdo-master-promote-packstack-scenario002',
    'weirdo-master-promote-packstack-scenario003',
    'weirdo-master-promote-puppet-openstack-scenario001',
    'weirdo-master-promote-puppet-openstack-scenario002',
    'weirdo-master-promote-puppet-openstack-scenario003',
    'weirdo-master-promote-puppet-openstack-scenario004',
    'weirdo-ocata-promote-packstack-scenario001',
    'weirdo-ocata-promote-packstack-scenario002',
    'weirdo-ocata-promote-packstack-scenario003',
    'weirdo-ocata-promote-puppet-openstack-scenario001',
    'weirdo-ocata-promote-puppet-openstack-scenario002',
    'weirdo-ocata-promote-puppet-openstack-scenario003',
    'weirdo-ocata-promote-puppet-openstack-scenario004'
)
TRIPLEOCI = {
    'console': '/console.html',
    'postci': '/logs/postci.txt',
    'ironic-conductor': '/logs/undercloud/var/log/ironic/ironic-conductor.txt',
    'syslog': '/logs/undercloud/var/log/messages',
    'logstash': '/logs/undercloud/var/log/extra/logstash.txt'
}

RDOCI = {
    'console': '/console.txt',
    "postci": '/undercloud/var/log/extra/logstash.txt',
    'ironic-conductor': '/undercloud/var/log/ironic/ironic-conductor.txt',
    'syslog': '/undercloud/var/log/messages',
    'logstash': '/undercloud/var/log/extra/logstash.txt'

}

PLUGIN = RDOCI
PLUGIN_JOBS = RDOCI_JOBS


class PLUGIN_RDOCI_CONFIG:
    console_name = 'console.txt'


class PLUGIN_TRIPLEOCI_CONFIG:
    console_name = 'console.html'


ACTIVE_PLUGIN_CONFIG = PLUGIN_RDOCI_CONFIG
