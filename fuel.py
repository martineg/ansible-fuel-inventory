#! /usr/bin/env python

import sys
import os
import subprocess
import optparse
import json
from collections import defaultdict

fuel = "/usr/bin/fuel"
fuel_cmd = "{0} node --json".format(fuel)

def _listnodes():
    p = subprocess.Popen(fuel_cmd.split(), stdout=subprocess.PIPE).stdout
    return json.load(p)

def fuel_inventory():
    inventory = defaultdict(list)
    inventory['_meta'] = {
        'hostvars' : {},
    }
    for node in _listnodes():
        hostname = node['name']
        inventory[node['roles']].append(hostname)
        nodemeta = {
            'online' : node['online'],
            'os_platform' : node['os_platform'],
            'status' : node['status'],
            'ip' : node['ip'],
            'mac' : node['mac'],
        }
        inventory['_meta']['hostvars'][hostname] = nodemeta
    return inventory

if __name__ == '__main__':
    if not os.path.exists(fuel):
        print json.dumps({})
        sys.exit(1)

    cli_parser = optparse.OptionParser()
    cli_parser.add_option('--list', action='store_true')
    cli_parser.add_option('--host', action='store', type='string')
    (options, args) = cli_parser.parse_args()

    inventory = fuel_inventory()
    if options.list:
        data = json.dumps(inventory)
        print data
    elif options.host:
        data = json.dumps(inventory['_meta']['hostvars'][options.host])
        print data
