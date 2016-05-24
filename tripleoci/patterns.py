import re

# Patterns regexps
timeout_re = re.compile(r"Killed\s+timeout -s 9 ")
puppet_re = re.compile(r"1;31mError: .+?\W(\w+)::")
resolving_re = re.compile(
    r"Could not resolve host: (\S+); Name or service not known")
exec_re = re.compile(r"mError: (\S+?) \S+ returned 1 instead of one of")
failed_deps_re = re.compile(r"Failed to build (.*)")
curl_re = re.compile(r"curl: \S*? couldn't open file \"(.*?)\"")
git_re = re.compile(r"fatal: Unable to look up (\S+)")
deploy_re = re.compile(r"Deployment exited with non-zero status code: (\d+)")

# Patterns to search in files
PATTERNS = {
    # file that should contain the pattern
    "/console.html": [

        {
            # ID of pattern
            "id": 1,
            # Pattern to search
            "pattern": "Stack overcloud CREATE_COMPLETE",
            # Message to print if pattern was found
            "msg": "Overcloud stack installation: SUCCESS.",
            # Tag that marks problem: infra, code, or nothing special
            "tag": "info",
            "logstash": '',
        },
        {
            "id": 2,
            "pattern": "Stack overcloud CREATE_FAILED",
            "msg": "Overcloud stack: FAILED.",
            "tag": "info",
            "logstash": 'Stack overcloud CREATE_FAILED',
        },
        {
            "id": 3,
            "pattern": "No valid host was found. There are not enough hosts",
            "msg": "No valid host was found.",
            "tag": "code",
            "logstash": 'No valid host was found. There are not enough hosts',
        },
        {
            "id": 4,
            "pattern": "Failed to connect to trunk.rdoproject.org port 80",
            "msg": "Connection failure to trunk.rdoproject.org.",
            "tag": "infra",
            "logstash": 'Failed to connect to trunk.rdoproject.org',
        },
        {
            "id": 5,
            "pattern": "Overloud pingtest, FAIL",
            "msg": "Overcloud pingtest FAILED.",
            "tag": "code",
            "logstash": '',
        },
        {
            "id": 6,
            "pattern": "Overcloud pingtest, failed",
            "msg": "Overcloud pingtest FAILED.",
            "tag": "code",
            "logstash": '',
        },
        {
            "id": 7,
            "pattern": "Error contacting Ironic server: Node ",
            "msg": "Ironic introspection FAIL.",
            "tag": "code",
            "logstash": 'Error contacting Ironic server: Node',
        },
        {
            "id": 8,
            "pattern": "Introspection completed with errors:",
            "msg": "Ironic introspection FAIL.",
            "tag": "code",
            "logstash": 'Introspection completed with errors:',
        },
        {
            "id": 9,
            "pattern": ": Introspection timeout",
            "msg": "Introspection timeout.",
            "tag": "code",
            "logstash": ': Introspection timeout',
        },
        {
            "id": 10,
            "pattern": "is locked by host localhost.localdomain, please retry",
            "msg": "Ironic: Host locking error.",
            "tag": "code",
            "logstash": '',
        },
        {
            "id": 11,
            "pattern": "Timed out waiting for node ",
            "msg": "Ironic node register FAIL: timeout for node.",
            "tag": "code",
            "logstash": 'Timed out waiting for node ',
        },
        {
            "id": 12,
            "pattern": "Killed                  ./testenv-client -b",
            "msg": "Killed by timeout.",
            "tag": "infra",
            'logstash': 'GATE_RETVAL=137'
        },
        {
            "id": 13,
            "pattern": timeout_re,
            "msg": "Killed by timeout.",
            "tag": "infra",
            'logstash': 'GATE_RETVAL=137'
        },
        {
            "id": 14,
            "pattern": puppet_re,
            "msg": "Puppet {} FAIL.",
            "tag": "code",
            "logstash": puppet_re,
        },
        {
            "id": 15,
            "pattern": exec_re,
            "msg": "Program {} FAIL.",
            "tag": "code",
            "logstash": exec_re,
        },
        {
            "id": 16,
            "pattern": "ERROR:dlrn:cmd failed. See logs at",
            "msg": "Delorean FAIL.",
            "tag": "code",
            'logstash': 'ERROR:dlrn:cmd failed. See logs at'
        },
        {
            "id": 17,
            "pattern": "500 Internal Server Error: Failed to upload image",
            "msg": "Glance upload FAIL.",
            "tag": "code",
            'logstash': '500 Internal Server Error: Failed to upload image'
        },
        {
            "id": 18,
            "pattern": "Slave went offline during the build",
            "msg": "Jenkins slave FAIL.",
            "tag": "infra",
            "logstash": '',
        },
        {
            "id": 19,
            "pattern": resolving_re,
            "msg": "DNS resolve of {} FAIL.",
            "tag": "infra",
            "logstash": resolving_re,
        },
        {
            "id": 20,
            "pattern": "fatal: The remote end hung up unexpectedly",
            "msg": "Git clone repo FAIL.",
            "tag": "infra",
            "logstash": 'fatal: The remote end hung up unexpectedly',
        },
        {
            "id": 21,
            "pattern": "Create timed out",
            "msg": "Overcloud create timed out.",
            "tag": "code",
            "logstash": '',
        },
        {
            "id": 22,
            "pattern": "[overcloud]: CREATE_FAILED Create timed out",
            "msg": "Overcloud create timed out.",
            "tag": "code",
            "logstash": '',
        },
        {
            "id": 23,
            "pattern": "FATAL: no longer a configured node for ",
            "msg": "Slave FAIL: no longer a configured node",
            "tag": "infra",
            "logstash": 'FATAL: no longer a configured node for',
        },
        {
            "id": 24,
            "pattern": ("cd: /opt/stack/new/delorean/data/repos: "
                        "No such file or directory"),
            "msg": "Delorean repo build FAIL.",
            "tag": "code",
            "logstash": ("cd: /opt/stack/new/delorean/data/repos: "
                         "No such file or directory"),
        },
        {
            "id": 25,
            "pattern": ("[ERROR] - SEVERE ERROR occurs: "
                        "java.lang.InterruptedException"),
            "msg": "Jenkins slave FAIL: InterruptedException",
            "tag": "infra",
            "logstash": '[ERROR] - SEVERE ERROR occurs: java.lang',
        },
        {
            "id": 26,
            "pattern": ("Killed                  bash -xe "
                        "/opt/stack/new/tripleo-ci/toci_gate_test.sh"),
            "msg": "Main script timeout",
            "tag": "infra",
            "logstash": ('Killed                  bash -xe '
                         '/opt/stack/new/tripleo-ci/toci_gate_test.sh')
        },
        {
            "id": 27,
            "pattern": ("Command 'instack-install-undercloud' "
                        "returned non-zero exit status"),
            "msg": "Undercloud install FAIL.",
            "tag": "code",
            'logstash': ('Command \'instack-install-undercloud\' '
                         'returned non-zero exit status'),
        },
        {
            "id": 28,
            "pattern": failed_deps_re,
            "msg": "Failed to build dep {}.",
            "tag": "infra",
            "logstash": failed_deps_re,
        },
        {
            "id": 29,
            "pattern": curl_re,
            "msg": "Failed to upload/get image: {}.",
            "tag": "infra",
            "logstash": curl_re,
        },
        {
            "id": 30,
            "pattern": "error: command 'gcc' failed with exit status 1",
            "msg": "Failed to compile deps.",
            "tag": "infra",
            "logstash": "error: command 'gcc' failed with exit status 1",
        },
        {
            "id": 31,
            "pattern": "crm_resource for openstack",
            "msg": "'crm_resource' check failed because timeout.",
            "tag": "infra",
            "logstash": 'crm_resource for openstack'
        },
        {
            "id": 32,
            "pattern": "failed to open 'instack.qcow2': No such file or",
            "msg": "FAIL to build image instack.qcow2.",
            "tag": "code",
            "logstash": "failed to open 'instack.qcow2': No such file or",
        },
        {
            "id": 33,
            "pattern": "Stack overcloud UPDATE_FAILED",
            "msg": "Stack update FAILED.",
            "tag": "info",
            "logstash": 'Stack overcloud UPDATE_FAILED',
        },
        {
            "id": 34,
            "pattern": git_re,
            "msg": "DNS resolve of {} FAIL.",
            "tag": "infra",
        },
        {
            "id": 35,
            "pattern": deploy_re,
            "msg": "Deployment exited with code {}.",
            "tag": "code",
        },
    ],

    '/logs/postci.txt.gz': [
        {
            "id": 202,
            "pattern": puppet_re,
            "msg": "Puppet {} FAIL.",
            "tag": "code",
            "logstash": puppet_re,
        },
        {
            "id": 202,
            "pattern": "Can't connect to local MySQL server through socket",
            "msg": "MySQL failure.",
            "tag": "code",
            "logstash": "Can't connect to local MySQL server through socket",
        },
    ],
    # '/logs/overcloud-controller-0.tar.xz//var/log/neutron/server.log': [
    #     {
    #         "id": 1849,
    #         "pattern": 'Extension router-service-type not supported',
    #         "msg": "Testing pattern, please ignore.",
    #         "tag": "code",
    #     },
    # ]
}
PATTERNS['/logs/postci.log'] = PATTERNS['/logs/postci.txt.gz']
