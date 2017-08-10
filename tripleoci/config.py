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
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-ocata-oooq',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-ha-newton-oooq',
    PERIODIC_LOGS_URL + '/periodic-tripleo-ci-centos-7-ovb-nonha-containers',
    PERIODIC_LOGS_URL +
    '/periodic-tripleo-ci-centos-7-ovb-nonha-tempest-oooq-ocata',
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
GERRIT_BRANCHES = ("master", "stable/newton", "stable/ocata")
PERIODIC_DAYS = 14
GATE_DAYS = 14
CIRCLE = 3
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
    'browbeat-quickstart-gerrit-newton-baremetal-CI',
    'browbeat-quickstart-gerrit-ocata-baremetal-CI',
    'browbeat-quickstart-gerrit-rhos-10-baremetal-CI',
    'browbeat-quickstart-master-baremetal-mixed',
    'browbeat-quickstart-master-baremetal-no_vlan',
    'browbeat-quickstart-master-baremetal-yoda',
    'browbeat-quickstart-newton-baremetal-mixed',
    'browbeat-quickstart-newton-baremetal-no_vlan',
    'browbeat-quickstart-newton-baremetal-yoda',
    'browbeat-quickstart-ocata-baremetal-mixed',
    'browbeat-quickstart-ocata-baremetal-no_vlan',
    'browbeat-quickstart-ocata-baremetal-yoda',
    'browbeat-quickstart-rhos-10-baremetal-mixed',
    'browbeat-quickstart-rhos-10-baremetal-no_vlan',
    'browbeat-quickstart-rhos-10-baremetal-yoda',
    'browbeat-quickstart-rhos-11-baremetal-mixed',
    'browbeat-quickstart-rhos-11-baremetal-no_vlan',
    'browbeat-quickstart-rhos-11-baremetal-yoda',
    'browbeat-quickstart-rhos-12-baremetal-mixed',
    'browbeat-quickstart-rhos-12-baremetal-no_vlan',
    'browbeat-quickstart-rhos-12-baremetal-yoda',
    'oooq-master-delorean-bmu-haa16-lab-float_nic_with_vlans',
    'oooq-newton-delorean-bmu-haa01-lab-float_nic_with_vlans',
    'oooq-ocata-rdo_trunk-bmu-haa01-lab-float_nic_with_vlans',
    'oooq-rhos-10-puddle-bmu-hac01-lab-float_nic_with_vlans',
    'oooq-rhos-11-puddle-bmu-hac01-lab-float_nic_with_vlans',
    'oooq-rhos-12-puddle-bmu-hab01-lab-float_nic_with_vlans',
    'oooq-rhos-12-puddle-bmu-had00-lab-float_nic_with_vlans',
    'osp-rhos-10-promote-puddle-build-images',
    'osp-rhos-10-promote-puddle-virtbasic-1ctlr_1comp_64gb',
    'osp-rhos-10-promote-puddle-virtha-3ctlr_1comp_192gb',
    'osp-rhos-11-promote-puddle-build-images',
    'osp-rhos-11-promote-puddle-virtbasic-1ctlr_1comp_64gb',
    'osp-rhos-11-promote-puddle-virtha-3ctlr_1comp_192gb',
    'osp-rhos-12-promote-puddle-build-images',
    'osp-rhos-12-promote-puddle-virtbasic-1ctlr_1comp_64gb',
    'osp-rhos-12-promote-puddle-virtha-3ctlr_1comp_192gb',
    'periodic-master-delorean-featureset010-1ctlr_1comp_64gb',
    'periodic-master-delorean-featureset016-1ctlr_1comp_64gb',
    'periodic-master-delorean-virtbasic-1ctlr_1comp_64gb',
    'periodic-master-delorean-virtbasic-1ctlr_1comp_64gb-arxcruz',
    'periodic-newton-delorean-virtbasic-1ctlr_1comp_64gb',
    'periodic-ocata-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
    ('poc-myoung_periodic-master-delorean-containers_minimal-'
     '1ctlr_1comp_64gb'),
    'promote-rhel-master-delorean-virtbasic-1ctlr_1comp_64gb',
    'promote-rhel-master-delorean-virtha-3ctlr_1comp_192gb',
    'promote-rhel-newton-delorean-virtbasic-1ctlr_1comp_64gb',
    'promote-rhel-newton-delorean-virtha-3ctlr_1comp_192gb',
    'promote-rhel-ocata-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
    'promote-rhel-ocata-rdo_trunk-virtha-3ctlr_1comp_192gb',
    'rdo-master-promote-delorean-build-images',
    'rdo-newton-promote-delorean-build-images',
    'rdo-ocata-promote-rdo_trunk-build-images',
    ('rlandy-poc-tripleo-quickstart-master-baremetal-hp_dl360_envE-'
     'single_nic_vlans'),
    ('tqe-gate-rhos-11-current-passed-ci-qeos7-ovb-minimal-pacemaker-'
     'public-bond'),
    'tq-gate-devmode-master-ovb-rdocloud-public-bond',
    ('tq-gate-rhos-11-current-passed-ci-qeos7-ovb-minimal-pacemaker-'
     'public-bond'),
    ('tripleo-quickstart-master-delorean-baremetal-dell_pe_r630-'
     'bond_with_vlans'),
    ('tripleo-quickstart-master-delorean-baremetal-hp_dl360_envD-'
     'single_nic_vlans'),
    ('tripleo-quickstart-newton-delorean-baremetal-dell_pe_r630-'
     'bond_with_vlans'),
    ('tripleo-quickstart-newton-delorean-baremetal-hp_dl360_envD-'
     'single_nic_vlans'),
    ('tripleo-quickstart-ocata-rdo_trunk-baremetal-dell_pe_r630-'
     'bond_with_vlans'),
    ('tripleo-quickstart-ocata-rdo_trunk-baremetal-hp_dl360_envD-'
     'single_nic_vlans'),
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
    main_index_timeout = 1100


class PLUGIN_TRIPLEOCI_CONFIG:
    console_name = 'console.html'

ACTIVE_PLUGIN_CONFIG = PLUGIN_RDOCI_CONFIG
COLUMNS = [{"Browbeat": "browbeat"}]
COLUMNS += [{
    i.replace('stable/', '').capitalize() + "-gate": i.replace('stable/', '')}
    for i in GERRIT_BRANCHES]
COLUMNS += [
{"OSP-10": "rhos-10"},
{"OSP-11": "rhos-11"},
{"OSP-12": "rhos-12"},
]
