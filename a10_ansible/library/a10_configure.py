
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pexpect
import re

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''

module: a10_configure
description:
    - a10_configure
short_description: Configures A10 write.memory
author: A10 Networks 2018
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    partition:
        description:
        - Destination/target partition for object/command
    console_command:
                description:
                - Console Commend


'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    console_command = ''
    module_args = dict(
	a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent"]),
        file_path=dict(type='str',),
        key_path=dict(type='str',),
        ip=dict(type='str',)
    )
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    ) 
    filename = module.params["file_path"]
    f = open(filename)
    f1 = f.readlines()
    child = pexpect.spawn('ssh -i '+module.params["key_path"]+" "+ module.params["a10_username"]+'@'+module.params["a10_host"])
    child.expect('>')
    child.sendline('enable')
    child.expect('Password:')
    child.sendline('')
    child.expect('#')
    child.sendline('configure')
    child.expect('#')
    for x in f1:
    	child.sendline(x.strip()+" "+module.params["ip"])
        child.expect('User name \[\]\?')
        child.sendline('admin')
	child.expect('#')
    a = child.before
    print a

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
