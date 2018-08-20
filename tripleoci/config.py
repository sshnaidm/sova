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
    'openstack/paunch',
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
WEB_TIMEOUT = (6.05, 15)
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/ocata", "stable/pike",
                   "stable/queens", "stable/rocky")
PERIODIC_DAYS = 14
GATE_DAYS = 14
CIRCLE = 3
COLUMNED_TRACKED_JOBS = {
    "Master": [
        'browbeat-quickstart-master-baremetal-mixed',
        'browbeat-quickstart-master-baremetal-yoda',
        'oooq-master-rdo_trunk-bmu-haa01-lab-float_nic_with_vlans',
        'oooq-master-rdo_trunk-bmu-haa16-lab-float_nic_with_vlans',
        'periodic-master-rdo_trunk-containers_minimal-1ctlr_1comp_64gb',
        'periodic-master-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'periodic-master-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'promote-rhel-master-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'promote-rhel-master-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'rdo-master-promote-rdo_trunk-build-images',
        'sbtest-tripleo-quickstart-extras-master-rdo_trunk',
        'sbtest-tripleo-quickstart-master-rdo_trunk',
        'tripleo-quickstart-master-ci-rhos-ovb-ha-multiple-nics',
        ('tripleo-quickstart-master-rdo_trunk-baremetal-dell_fc430_envB-'
         'single_nic_vlans'),
        ('tripleo-quickstart-master-rdo_trunk-baremetal-dell_pe_r630-'
         'bond_with_vlans'),
        ('tripleo-quickstart-master-rdo_trunk-baremetal-hp_dl360_envD-'
         'single_nic_vlans'),
        ('tripleo-quickstart-master-rdo_trunk-baremetal-hp_dl360_envE-'
         'single_nic_vlans'),
    ],
    "Pike": [
        'browbeat-quickstart-pike-baremetal-mixed',
        'browbeat-quickstart-pike-baremetal-yoda',
        'periodic-pike-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'periodic-pike-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'oooq-pike-rdo_trunk-bmu-haa01-lab-float_nic_with_vlans',
        'oooq-pike-rdo_trunk-bmu-haa16-lab-float_nic_with_vlans',
        'promote-rhel-pike-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'promote-rhel-pike-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'rdo-pike-promote-rdo_trunk-build-images',
        'sbtest-tripleo-quickstart-extras-pike-rdo_trunk',
        'sbtest-tripleo-quickstart-pike-rdo_trunk',
        'tripleo-quickstart-pike-ci-rhos-ovb-ha-multiple-nics',
        ('tripleo-quickstart-pike-rdo_trunk-baremetal-dell_fc430_envB-'
         'single_nic_vlans'),
        ('tripleo-quickstart-pike-rdo_trunk-baremetal-dell_pe_r630-'
         'bond_with_vlans'),
        ('tripleo-quickstart-pike-rdo_trunk-baremetal-hp_dl360_envD-'
         'single_nic_vlans'),
        ('tripleo-quickstart-pike-rdo_trunk-baremetal-hp_dl360_envE-'
         'single_nic_vlans')
    ],
    "Ocata": [
        'browbeat-quickstart-gerrit-ocata-baremetal-CI',
        'browbeat-quickstart-ocata-baremetal-mixed',
        'browbeat-quickstart-ocata-baremetal-yoda',
        'oooq-ocata-rdo_trunk-bmu-haa01-lab-float_nic_with_vlans',
        'oooq-ocata-rdo_trunk-bmu-haa16-lab-float_nic_with_vlans',
        'periodic-ocata-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'periodic-ocata-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'promote-rhel-ocata-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'promote-rhel-ocata-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'rdo-ocata-promote-rdo_trunk-build-images',
        'sbtest-tripleo-quickstart-extras-ocata-rdo_trunk',
        'sbtest-tripleo-quickstart-ocata-rdo_trunk',
        ('tqe-upgrades-gate-ocata-undercloud-newton-overcloud-ci-rhos-'
         'composable_upgrade_ovb'),
        ('tripleo-quickstart-ocata-rdo_trunk-baremetal-dell_fc430_envB-'
         'single_nic_vlans'),
        ('tripleo-quickstart-ocata-rdo_trunk-baremetal-dell_pe_r630-'
         'bond_with_vlans'),
        ('tripleo-quickstart-ocata-rdo_trunk-baremetal-hp_dl360_envD-'
         'single_nic_vlans'),
        ('tripleo-quickstart-ocata-rdo_trunk-baremetal-hp_dl360_envE-'
         'single_nic_vlans'),
    ],
    "Newton": [
        'browbeat-quickstart-newton-baremetal-mixed',
        'browbeat-quickstart-newton-baremetal-yoda',
        'oooq-newton-rdo_trunk-bmu-haa01-lab-float_nic_with_vlans',
        'oooq-newton-rdo_trunk-bmu-haa16-lab-float_nic_with_vlans',
        'periodic-newton-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'periodic-newton-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'promote-rhel-newton-rdo_trunk-virtbasic-1ctlr_1comp_64gb',
        'promote-rhel-newton-rdo_trunk-virtha-3ctlr_1comp_192gb',
        'rdo-newton-promote-rdo_trunk-build-images',
        'sbtest-tripleo-quickstart-extras-newton-rdo_trunk',
        'sbtest-tripleo-quickstart-newton-rdo_trunk',
        ('tripleo-quickstart-newton-rdo_trunk-baremetal-dell_fc430_envB-'
         'single_nic_vlans'),
        ('tripleo-quickstart-newton-rdo_trunk-baremetal-dell_pe_r630-'
         'bond_with_vlans'),
        ('tripleo-quickstart-newton-rdo_trunk-baremetal-hp_dl360_envD-'
         'single_nic_vlans'),
        ('tripleo-quickstart-newton-rdo_trunk-baremetal-hp_dl360_envE-'
         'single_nic_vlans'),
    ],
    "RHOS 8": [
        'oooq-rhos-8-poodle-bmu-hab01-lab-float_nic_with_vlans',
        'oooq-rhos-8-poodle-bmu-hac01-lab-float_nic_with_vlans',
        'osp-rhos-8-promote-poodle-virtbasic-1ctlr_1comp_64gb',
        'osp-rhos-8-promote-poodle-virtha-3ctlr_1comp_64gb',
    ],
    "RHOS 9": [
        'oooq-rhos-9-poodle-bmu-hab01-lab-float_nic_with_vlans',
        'oooq-rhos-9-poodle-bmu-hac01-lab-float_nic_with_vlans',
        'osp-rhos-9-promote-poodle-virtbasic-1ctlr_1comp_64gb',
        'osp-rhos-9-promote-poodle-virtha-3ctlr_1comp_64gb',
    ],
    "RHOS 10": [
        'browbeat-quickstart-gerrit-rhos-10-baremetal-CI',
        'browbeat-quickstart-rhos-10-baremetal-mixed',
        'browbeat-quickstart-rhos-10-baremetal-yoda',
        'oooq-rhos-10-puddle-bmu-hab01-lab-float_nic_with_vlans',
        'oooq-rhos-10-puddle-bmu-hac01-lab-float_nic_with_vlans',
        'osp-rhos-10-promote-puddle-virtbasic-1ctlr_1comp_64gb',
        'osp-rhos-10-promote-puddle-virtha-3ctlr_1comp_192gb',
        'sbtest-tripleo-quickstart-extras-rhos-10-puddle',
        'sbtest-tripleo-quickstart-rhos-10-puddle',
    ],
    "RHOS 11": [
        'browbeat-quickstart-rhos-11-baremetal-mixed',
        'browbeat-quickstart-rhos-11-baremetal-yoda',
        'oooq-rhos-11-puddle-bmu-hab01-lab-float_nic_with_vlans',
        'oooq-rhos-11-puddle-bmu-hac01-lab-float_nic_with_vlans',
        'osp-rhos-11-promote-puddle-virtbasic-1ctlr_1comp_64gb',
        'osp-rhos-11-promote-puddle-virtha-3ctlr_1comp_192gb',
        'sbtest-tripleo-quickstart-extras-rhos-11-puddle',
        'sbtest-tripleo-quickstart-rhos-11-puddle',
        'tq-gate-rhos-11-ci-rhos-ovb-minimal-pacemaker-public-bond',
        'tqe-gate-rhos-11-ci-rhos-ovb-minimal-pacemaker-public-bond',
    ],
    "RHOS 12": [
        'browbeat-quickstart-rhos-12-baremetal-mixed',
        'browbeat-quickstart-rhos-12-baremetal-yoda',
        'oooq-rhos-12-puddle-bmu-hab01-lab-float_nic_with_vlans',
        'oooq-rhos-12-puddle-bmu-hac01-lab-float_nic_with_vlans',
        'oooq-rhos-12-puddle-bmu-had00-lab-float_nic_with_vlans',
        'osp-rhos-12-promote-puddle-virtbasic-1ctlr_1comp_64gb',
        'osp-rhos-12-promote-puddle-virtha-3ctlr_1comp_192gb',
        'sbtest-tripleo-quickstart-extras-rhos-12-puddle',
        'sbtest-tripleo-quickstart-rhos-12-puddle',
    ]
}

RDOCI = {
    'console': '/console.txt.gz',
    "postci": '/undercloud/var/log/extra/logstash.txt',
    'ironic-conductor': '/undercloud/var/log/ironic/ironic-conductor.txt',
    'syslog': '/undercloud/var/log/messages',
    'logstash': '/undercloud/var/log/extra/logstash.txt'

}

PLUGIN = RDOCI
TRACKED_JOBS = [k for i in COLUMNED_TRACKED_JOBS.values() for k in i]
PLUGIN_JOBS = TRACKED_JOBS


class PLUGIN_RDOCI_CONFIG:
    console_name = 'console.txt.gz'
    main_index_timeout = 1100


ACTIVE_PLUGIN_CONFIG = PLUGIN_RDOCI_CONFIG
