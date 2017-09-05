#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
import ast
import traceback
import time

from ansible.module_utils.basic import AnsibleModule

try:
    from bonita.api.bonita_client import BonitaClient
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

    def __init__(self, module, verbose=False):
        self.module = module
        self.logs = []

    def log(self, s):
        self.logs.append(s)
        logging.getLogger(LOGGER_NAME).debug(s)


def main():
    module = AnsibleModule(
        argument_spec={
            "session": {'type': 'str', 'default': None, 'choices': ['login','logout','get']},
            "platform": {'type': 'str', 'default': None},
            "process": {'type': 'str', 'default': None},
            "system": {'type': 'str', 'default': None},
            "upload": {'type': 'str', 'default': None},
            "session": {'type': 'str', 'default': None},
            # Configuration
            "configuration": {'type': 'path', 'default': '~/.bonita'},
            # Session parameters
            "url": {'type': 'str', 'default': None},
            "username": {'type': 'str', 'default': None},
            "password": {'type': 'str', 'default': None},
            # Global
            "verbose": {'type': 'bool', 'default': False}
        }
    )

    verbose = module.params['verbose']

    if verbose:
        logging.basicConfig(filename=LOGGER_FILE,
                            level=logging.DEBUG)
        LOGGER.debug('--- %s ---', time.strftime("%H:%M:%S"))
    else:
        LOGGER.setLevel(logging.INFO)

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