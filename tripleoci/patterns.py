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
hiera_re = re.compile(r"Error: Could not find data item (\w+) in any Hiera "
                      r"data file and no default supplied")
puppetexec_re = re.compile(r"mError: /Stage\[main\]/\w+/Exec\[(.+?)\]")
command_exe = re.compile(r"Job for (.+) failed because the control "
                         r"process exited with error code.")
zcl_re = re.compile(r"stderr: 'fatal: unable to access "
                    r"'http.+/devstack-gate/.*Network is unreachable.*")
gitnet_re = re.compile(
    r"fatal: unable to access 'http.*Network is unreachable")
ssh_re = re.compile(r"ssh: connect to host .+ port .+: No route to host")
pup_module_re = re.compile(r'mError: .* at /etc/puppet/modules/([^/]+)/')
service_fail_re = re.compile(r"systemd: (\S+).service failed")
fail_refresh_re = re.compile(r"\[([\w-]+)\]: Failed to call refresh")
iron_space_re = re.compile(r"Disk volume where .* "
                           r"is located doesn't have enough disk space")

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
            "pattern": "ERROR:dlrn:",
            "msg": "Delorean FAIL.",
            "tag": "code",
            'logstash': 'ERROR:dlrn:'
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
            "logstash": git_re,
        },
        {
            "id": 35,
            "pattern": deploy_re,
            "msg": "Deployment exited with code {}.",
            "tag": "code",
            "logstash": deploy_re,
        },
        {
            "id": 36,
            "pattern": 'Error: No connected Gearman servers',
            "msg": "Gearman problem.",
            "tag": "infra",
            "logstash": "No connected Gearman servers",
        },
        {
            "id": 37,
            "pattern": 'Overcloud pingtest FAILED',
            "msg": "Overcloud pingtest FAILED.",
            "tag": "code",
            "logstash": "Overcloud pingtest FAILED",
        },
        {
            "id": 38,
            "pattern": '... FAILED',
            "msg": "Tempest tests FAILED.",
            "tag": "code",
            "logstash": "... FAILED",
        },
        {
            "id": 39,
            "pattern": 'No more mirrors to try',
            "msg": "Network issue 'No more mirrors'.",
            "tag": "infra",
            "logstash": "No more mirrors to try",
        },
        {
            "id": 40,
            "pattern": 'ERROR - The gearman Job has failed',
            "msg": "Gearman task FAILED.",
            "tag": "infra",
            "logstash": "The gearman Job has failed",
        },
        {
            "id": 41,
            "pattern": "ERROR - Couldn't retrieve env",
            "msg": "Environment setup FAILED.",
            "tag": "infra",
            "logstash": "ERROR - Couldn't retrieve env",
        },
        {
            "id": 42,
            "pattern": ('Command "python setup.py egg_info" '
                        'failed with error code 1'),
            "msg": "Pip install FAIL.",
            "tag": "infra",
            "logstash": ("Command \"python setup.py egg_info\" "
                         "failed with error code 1"),
        },
        {
            "id": 43,
            "pattern": ('MessagingTimeout: Timed out waiting for a reply '
                        'to message ID'),
            "msg": "Message timeout.",
            "tag": "code",
            "logstash": ("MessagingTimeout: Timed out waiting for a reply "
                         "to message ID"),
        },
        {
            "id": 44,
            "pattern": ("504 Gateway Time-out: "
                        "The server didn't respond in time"),
            "msg": "Gateway timeout 504.",
            "tag": "infra",
            "logstash": ("504 Gateway Time-out: "
                         "The server didn't respond in time"),
        },
        {
            "id": 45,
            "pattern": "Exception registering nodes:",
            "msg": "Node registration FAIL.",
            "tag": "code",
            "logstash": "Exception registering nodes:",
        },
        {
            "id": 46,
            "pattern": ("400 Bad Request: Client disconnected before "
                        "sending all data to backend (HTTP 400)"),
            "msg": "HTTP 400 Error.",
            "tag": "code",
            "logstash": ("400 Bad Request: Client disconnected before "
                         "sending all data to backend (HTTP 400)"),
        },
        {
            "id": 47,
            "pattern": command_exe,
            "msg": "{} FAIL.",
            "tag": "code",
            "logstash": command_exe,
        },
        {
            "id": 48,
            "pattern": zcl_re,
            "msg": "Zuul-cloner network FAIL.",
            "tag": "infra",
            "logstash": 'Network is unreachable',
        },
        {
            "id": 49,
            "pattern": gitnet_re,
            "msg": "Network FAIL.",
            "tag": "infra",
            "logstash": 'Network is unreachable',
        },
        {
            "id": 50,
            "pattern": ssh_re,
            "msg": "SSH to host FAIL.",
            "tag": "code",
            "logstash": 'port 22: No route to host',
        },
        {
            "id": 51,
            "pattern": "CommandError: No image with a name or ID of",
            "msg": "No image on the host.",
            "tag": "code",
            "logstash": 'CommandError: No image with a name or ID of',
        },
        {
            "id": 52,
            "pattern": "Not enough nodes - available",
            "msg": "Not enough nodes are available.",
            "tag": "code",
            "logstash": 'Not enough nodes - available',
        },
        {
            "id": 53,
            "pattern": "Timing out after 300 seconds:",
            "msg": "Pingtest stack timeout.",
            "tag": "code",
            "logstash": 'Timing out after 300 seconds:',
        },
        {
            "id": 54,
            "pattern": "504 Gateway Time-out",
            "msg": "504 Gateway Time-out.",
            "tag": "code",
            "logstash": '504 Gateway Time-out',
        },
        {
            "id": 55,
            "pattern": "Gateway Time-out (HTTP 504)",
            "msg": "504 Gateway Time-out.",
            "tag": "code",
            "logstash": 'Gateway Time-out (HTTP 504)',
        },
        {
            "id": 56,
            "pattern": ("Retrying (Retry(total=0, connect=None, read=None, "
                        "redirect=None)) after connection broken by"),
            "msg": "Pip networking timeout.",
            "tag": "infra",
            "logstash": ("Retrying (Retry(total=0, connect=None, read=None, "
                         "redirect=None)) after connection broken by"),
        },
    ],

    '/logs/postci.txt': [
        {
            "id": 200,
            "pattern": puppet_re,
            "msg": "Puppet {} FAIL.",
            "tag": "code",
            "logstash": puppet_re,
        },
        {
            "id": 201,
            "pattern": "Can't connect to local MySQL server through socket",
            "msg": "MySQL failure.",
            "tag": "code",
            "logstash": "Can't connect to local MySQL server through socket",
        },
        {
            "id": 202,
            "pattern": "Could not evaluate: Cannot allocate memory - fork(2)",
            "msg": "Puppet memory fail.",
            "tag": "infra",
            "logstash": "Could not evaluate: Cannot allocate memory - fork",
        },
        {
            "id": 203,
            "pattern": hiera_re,
            "msg": "No {} in Hiera.",
            "tag": "code",
            "logstash": hiera_re,
        },
        {
            "id": 204,
            "pattern": hiera_re,
            "msg": "No {} in Hiera.",
            "tag": "code",
            "logstash": hiera_re,
        },
        {
            "id": 205,
            "pattern": puppetexec_re,
            "msg": "{} FAIL.",
            "tag": "code",
            "logstash": puppetexec_re,
        },
        {
            "id": 206,
            "pattern": pup_module_re,
            "msg": "Puppet module '{}' FAIL.",
            "tag": "code",
            "logstash": pup_module_re,
        },
        {
            "id": 207,
            "pattern": fail_refresh_re,
            "msg": "{} FAIL.",
            "tag": "code",
            "logstash": fail_refresh_re,
        },
    ],

    '/logs/undercloud/var/log/ironic/ironic-conductor.txt': [
        {
            "id": 300,
            "pattern": "Timeout reached while waiting for callback for node",
            "msg": "Ironic deployment timeout.",
            "tag": "code",
            "logstash": "Timeout reached while waiting for callback for node",
        },
        {
            "id": 301,
            "pattern": iron_space_re,
            "msg": "No space on disk for Ironic.",
            "tag": "infra",
            "logstash": "is located doesn't have enough disk space. Required",
        },

    ],
    '/logs/undercloud/var/log/messages': [
        {
            "id": 400,
            "pattern": service_fail_re,
            "msg": "{} service FAIL.",
            "tag": "code",
            "logstash": "",
            "exclude": ["glean@", "docker-storage-setup"]
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
