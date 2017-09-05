#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
import ast
import traceback
import time
import sys

from ansible.module_utils.basic import AnsibleModule

try:
    import bonita.commands
    from inspect import getmembers, isclass, getmodule      
    HAS_BONITA_CLI = True
except:
    
    HAS_BONITA_CLI = False

DOCUMENTATION = '''
---
module: bonita
short_description: Module to manage Bonita platform from Ansible
'''

EXAMPLES = '''
- name: Login to Bonita
  bonita:
    session: login
    url: "{{ bonita_url }}"
    username: "{{bonita_credentials.username}}"
    password: "{{bonita_credentials.passwod}}"
- name: Get session
  bonita:
    session: get
  register: bonita_session
- name: Display session
  debug: msg="{{ bonita_session }}"
- name: Login to platform and use alternate configuration location
  bonita:
    platform: login
    url: "{{ bonita_url }}"
    username: "{{bonita_platform_credentials.username}}"
    password: "{{bonita_platform_credentials.passwod}}"
    configuration: "{{ playbook_dir + '/.bonita' }}"    
- name: Stop platform
  bonita:
    platform: stop
  register: stop_result_code
- name: Get platform
  bonita:
    platform: get
...
'''

LOGGER_NAME = 'bonita_module'
LOGGER_FILE = '/tmp/' + LOGGER_NAME + '.log'
LOGGER = logging.getLogger(LOGGER_NAME)
    
class Bonita:
    """
    Class used to centralize the operations with Bonita
    """

    def __init__(self, options, verbose=False):
        self.options = options
        self.logs = []

    def run(self):
        for (k, v) in self.options.items(): 
            if hasattr(bonita.commands, k) and v:
                module = getattr(bonita.commands, k)
                bonita.commands = getmembers(module, isclass)
                command = [command[1] for command in bonita.commands if command[0] != 'Base' and getmodule(command[1]).__name__.startswith('bonita.commands') ][0]
                command = command(self.options)
                command.run()

    def log(self, s):
        self.logs.append(s)
        logging.getLogger(LOGGER_NAME).debug(s)


def main():
    module = AnsibleModule(
        argument_spec={
            "args": {'type': 'dict', 'required': True},
            "verbose": {'type': 'bool', 'default': 'false'}
        }
    )

    verbose = module.params['verbose']

    if verbose:
        logging.basicConfig(filename=LOGGER_FILE,
                            level=logging.DEBUG)
        LOGGER.debug('--- %s ---', time.strftime("%H:%M:%S"))
        LOGGER.debug(sys.path)
    else:
        LOGGER.setLevel(logging.INFO)

    LOGGER.debug('Bonita cli available: %s' % HAS_BONITA_CLI)
    bonita_cli = Bonita(module.params['args'])
    bonita_cli.run()

    result = dict() 
    result['rc'] = 200

    fact = None
    changed = True
    if fact is not None:
        ansible_facts = dict()
        ansible_facts[fact] = result
        module.exit_json(changed=changed, result=result,
                         ansible_facts=ansible_facts)
    else:
        module.exit_json(changed=changed, result=result)

if __name__ == '__main__':
    main()