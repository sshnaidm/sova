import logging
import os


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('watchcat')
log.setLevel(logging.DEBUG)

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
    'openstack/puppet-pacemaker',
    'openstack/puppet-tripleo',
    'openstack/tripleo-docs',
    'openstack/tripleo-quickstart',
    'openstack/tripleo-specs',
    'openstack/tripleo-ui',
)

PERIODIC_URLS = [
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-ha-liberty/',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-ha-mitaka/',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-ha/',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-nonha/',
    'http://logs.openstack.org/periodic/periodic-tripleo-ci-f22-upgrades/',
]

DOWNLOAD_PATH = os.path.join(os.environ["HOME"], "ci_status")
SSH_TIMEOUT = 120
GERRIT_REQ_TIMEOUT = 2
GERRIT_PATCH_LIMIT = 200
GERRIT_HOST = "review.openstack.org"
GERRIT_PORT = 29418
GERRIT_USER = "robo"
GERRIT_BRANCHES = ("master", "stable/liberty", "stable/mitaka")
TRACKED_JOBS = ("gate-tripleo-ci-f22-upgrades",
                "gate-tripleo-ci-f22-nonha",
                "gate-tripleo-ci-f22-ha",
                "gate-tripleo-ci-f22-containers")
