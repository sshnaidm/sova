import re

# Patterns regexps
timeout_re = re.compile(r"Killed\s+timeout -s 9 ")
puppet_re = re.compile(r"\"deploy_stderr\": \".+?1;31mError: .+?\W(\w+)::")
resolving_re = re.compile(
    r"Could not resolve host: (\S+); Name or service not known")
exec_re = re.compile(r"mError: (\S+?) \S+ returned 1 instead of one of")
failed_deps_re = re.compile(r"Failed to build (.*)")
curl_re = re.compile(r"curl: \S*? couldn't open file \"(.*?)\"")

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
        },
        {
            "id": 2,
            "pattern": "Stack overcloud CREATE_FAILED",
            "msg": "Overcloud stack: FAILED.",
            "tag": "info",
        },
        {
            "id": 3,
            "pattern": "No valid host was found. There are not enough hosts",
            "msg": "No valid host was found.",
            "tag": "code",
        },
        {
            "id": 4,
            "pattern": "Failed to connect to trunk.rdoproject.org port 80",
            "msg": "Connection failure to trunk.rdoproject.org.",
            "tag": "infra",
        },
        {
            "id": 5,
            "pattern": "Overloud pingtest, FAIL",
            "msg": "Overcloud pingtest FAILED.",
            "tag": "code",
        },
        {
            "id": 6,
            "pattern": "Overcloud pingtest, failed",
            "msg": "Overcloud pingtest FAILED.",
            "tag": "code",
        },
        {
            "id": 7,
            "pattern": "Error contacting Ironic server: Node ",
            "msg": "Ironic introspection FAIL.",
            "tag": "code",
        },
        {
            "id": 8,
            "pattern": "Introspection completed with errors:",
            "msg": "Ironic introspection FAIL.",
            "tag": "code",
        },
        {
            "id": 9,
            "pattern": ": Introspection timeout",
            "msg": "Introspection timeout.",
            "tag": "code",
        },
        {
            "id": 10,
            "pattern": "is locked by host localhost.localdomain, please retry",
            "msg": "Ironic: Host locking error.",
            "tag": "code",
        },
        {
            "id": 11,
            "pattern": "Timed out waiting for node ",
            "msg": "Ironic node register FAIL: timeout for node.",
            "tag": "code",
        },
        {
            "id": 12,
            "pattern": "Killed                  ./testenv-client -b",
            "msg": "Killed by timeout.",
            "tag": "infra",
        },
        {
            "id": 13,
            "pattern": timeout_re,
            "msg": "Killed by timeout.",
            "tag": "infra",
        },
        {
            "id": 14,
            "pattern": puppet_re,
            "msg": "Puppet {} FAIL.",
            "tag": "code",
        },
        {
            "id": 15,
            "pattern": exec_re,
            "msg": "Program {} FAIL.",
            "tag": "code",
        },
        {
            "id": 16,
            "pattern": "ERROR:dlrn:cmd failed. See logs at",
            "msg": "Delorean FAIL.",
            "tag": "code",
        },
        {
            "id": 17,
            "pattern": "500 Internal Server Error: Failed to upload image",
            "msg": "Glance upload FAIL.",
            "tag": "code",
        },
        {
            "id": 18,
            "pattern": "Slave went offline during the build",
            "msg": "Jenkins slave FAIL.",
            "tag": "infra",
        },
        {
            "id": 19,
            "pattern": resolving_re,
            "msg": "DNS resolve of {} FAIL.",
            "tag": "infra",
        },
        {
            "id": 20,
            "pattern": "fatal: The remote end hung up unexpectedly",
            "msg": "Git clone repo FAIL.",
            "tag": "infra",
        },
        {
            "id": 21,
            "pattern": "Create timed out       | CREATE_FAILED",
            "msg": "Overcloud create timed out.",
            "tag": "code",
        },
        {
            "id": 22,
            "pattern": "[overcloud]: CREATE_FAILED Create timed out",
            "msg": "Overcloud create timed out.",
            "tag": "code",
        },
        {
            "id": 23,
            "pattern": "FATAL: no longer a configured node for ",
            "msg": "Slave FAIL: no longer a configured node",
            "tag": "infra",
        },
        {
            "id": 24,
            "pattern": ("cd: /opt/stack/new/delorean/data/repos: "
                        "No such file or directory"),
            "msg": "Delorean repo build FAIL.",
            "tag": "code",
        },
        {
            "id": 25,
            "pattern": ("[ERROR] - SEVERE ERROR occurs: "
                        "java.lang.InterruptedException"),
            "msg": "Jenkins slave FAIL: InterruptedException",
            "tag": "infra",
        },
        {
            "id": 26,
            "pattern": ("Killed                  bash -xe "
                        "/opt/stack/new/tripleo-ci/toci_gate_test.sh"),
            "msg": "Main script timeout",
            "tag": "infra",
        },
        {
            "id": 27,
            "pattern": ("Command 'instack-install-undercloud' "
                        "returned non-zero exit status"),
            "msg": "Undercloud install FAIL.",
            "tag": "code",
        },
        {
            "id": 28,
            "pattern": failed_deps_re,
            "msg": "Failed to build dep {}.",
            "tag": "infra",
        },
        {
            "id": 29,
            "pattern": curl_re,
            "msg": "Failed to upload/get image: {}.",
            "tag": "infra"
        },
        {
            "id": 30,
            "pattern": "error: command 'gcc' failed with exit status 1",
            "msg": "Failed to compile deps.",
            "tag": "infra"
        },
        {
            "id": 31,
            "pattern": "Killed by signal 15.",
            "msg": "'crm_resource' check failed because timeout.",
            "tag": "infra"
        },
    ],

    '/logs/postci.log': [
        {
            "id": 201,
            "pattern": puppet_re,
            "msg": "Puppet {} FAIL.",
            "tag": "code",
        },
    ],
    '/logs/postci.txt.gz': [
        {
            "id": 202,
            "pattern": puppet_re,
            "msg": "Puppet {} FAIL.",
            "tag": "code",
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
