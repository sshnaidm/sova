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
    'openstack/tripleo-specs',
    'openstack/tripleo-ui',
    '^openstack/puppet-.*',

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
GERRIT_BRANCHES = ("master", "stable/newton", "stable/ocata", "stable/pike",
                   "stable/queens")
PERIODIC_DAYS = 14
GATE_DAYS = 14
CIRCLE = 3
COLUMNED_TRACKED_JOBS = {
    "Newton": [
        'rdo-delorean-promote-newton',
        'tripleo-quickstart-gate-newton-delorean-full-minimal_pacemaker',
        'tripleo-quickstart-gate-newton-delorean-quick-basic',
        'tripleo-quickstart-periodic-newton-delorean-ooo-snap-minimal',
        'tripleo-quickstart-promote-newton-cloudsig-stable-build-images',
        'tripleo-quickstart-promote-newton-cloudsig-stable-minimal',
        'tripleo-quickstart-promote-newton-cloudsig-stable-minimal_pacemaker',
        'tripleo-quickstart-promote-newton-cloudsig-testing-build-images',
        'tripleo-quickstart-promote-newton-cloudsig-testing-minimal',
        'tripleo-quickstart-promote-newton-cloudsig-testing-minimal_pacemaker',
        'tripleo-quickstart-promote-newton-delorean-build-images',
        'tripleo-quickstart-promote-newton-delorean-minimal',
        'tripleo-quickstart-promote-newton-delorean-minimal_pacemaker',
    ],
    "Ocata": [
        'rdo-promote-get-hash-ocata-current-triple',
        'rdo_trunk-promote-ocata-current-tripleo',
        'tripleo-dlrn-promote-ocata',
        'tripleo-quickstart-gate-ocata-delorean-full-minimal',
        'tripleo-quickstart-gate-ocata-delorean-quick-basic',
        'tripleo-quickstart-gate-ocata-full-images',
        'tripleo-quickstart-promote-ocata-build-images',
        'tripleo-quickstart-promote-ocata-cloudsig-stable-build-images',
        'tripleo-quickstart-promote-ocata-cloudsig-stable-minimal_pacemaker',
        'tripleo-quickstart-promote-ocata-cloudsig-testing-build-images',
        'tripleo-quickstart-promote-ocata-cloudsig-testing-minimal',
        'tripleo-quickstart-promote-ocata-cloudsig-testing-minimal_pacemaker',
        'tripleo-quickstart-promote-ocata-rdo_trunk-minimal',
        'tripleo-quickstart-promote-ocata-rdo_trunk-minimal_pacemaker',
        'weirdo-ocata-promote-packstack-scenario001',
        'weirdo-ocata-promote-packstack-scenario002',
        'weirdo-ocata-promote-packstack-scenario003',
        'weirdo-ocata-promote-puppet-openstack-scenario001',
        'weirdo-ocata-promote-puppet-openstack-scenario002',
        'weirdo-ocata-promote-puppet-openstack-scenario003',
        'weirdo-ocata-promote-puppet-openstack-scenario004'
    ],
    "Pike": [
        "tripleo-quickstart-promote-pike-rdo_trunk-minimal",
        "tripleo-quickstart-promote-pike-rdo_trunk-minimal_pacemaker",
        "weirdo-pike-promote-packstack-scenario001",
        "weirdo-pike-promote-packstack-scenario002",
        "weirdo-pike-promote-packstack-scenario003",
        "weirdo-pike-promote-puppet-openstack-scenario001",
        "weirdo-pike-promote-puppet-openstack-scenario002",
        "weirdo-pike-promote-puppet-openstack-scenario003",
        "weirdo-pike-promote-puppet-openstack-scenario004",
    ],
    "Master": [
        'rdo-promote-build-images-master',
        'rdo-promote-get-hash-master',
        'rdo-promote-get-hash-master-current-tripleo',
        'rdo_trunk-promote-master-current-tripleo',
        'tripleo-quickstart-gate-master-delorean-full-minimal',
        'tripleo-quickstart-gate-master-delorean-quick-basic',
        'tripleo-quickstart-gate-master-full-images',
        'tripleo-quickstart-gate-master-tripleo-ci-delorean-full-minimal',
        'tripleo-quickstart-periodic-master-delorean-images-minimal_pacemaker',
        'tripleo-quickstart-promote-master-build-images',
        'tripleo-quickstart-promote-master-current-tripleo-delorean-minimal',
        ('tripleo-quickstart-promote-master-current-tripleo-delorean-'
        'minimal_pacemaker'),
        'tripleo-quickstart-promote-master-delorean-minimal',
        'tripleo-quickstart-promote-master-delorean-minimal_pacemaker',
        'tripleo-quickstart-upgrade-major-mitaka-to-master',
        'weirdo-master-promote-packstack-scenario001',
        'weirdo-master-promote-packstack-scenario002',
        'weirdo-master-promote-packstack-scenario003',
        'weirdo-master-promote-puppet-openstack-scenario001',
        'weirdo-master-promote-puppet-openstack-scenario002',
        'weirdo-master-promote-puppet-openstack-scenario003',
        'weirdo-master-promote-puppet-openstack-scenario004',
    ],
    "Patches": [
        ('tqe-containers-gate-master-tripleo-ci-delorean-'
         'full-containers_minimal'),
        'tripleo-quickstart-extras-gate-newton-delorean-full-minimal',
        ('tripleo-quickstart-extras-gate-master-tripleo-'
         'ci-delorean-full-minimal_pacemaker'),
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
