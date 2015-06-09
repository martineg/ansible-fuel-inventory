#! /usr/bin/env python

import sys
import os
import subprocess
import optparse
import json
from collections import defaultdict
from ConfigParser import ConfigParser

fuel = "/usr/bin/fuel"
fuel_cmd = "{0} node --json".format(fuel)

inventory_path = os.path.dirname(os.path.realpath(__file__))
inventory_ini = inventory_path + os.path.sep + 'fuel.ini'
inventory_cfg = {
    'skip_deleting' : False,
    'skip_offline'  : False,
}

def _read_config():
    if not os.path.exists(inventory_ini):
        return

    c = ConfigParser()
    c.read(inventory_ini)

    if not c.has_section('fuel'):
        return
    for option in ('skip_deleting', 'skip_offline'):
        if c.has_option('fuel', option):
            inventory_cfg[option] = c.getboolean('fuel', option)

def _listnodes():
    p = subprocess.Popen(fuel_cmd.split(), stdout=subprocess.PIPE).stdout
    return json.load(p)

def fuel_inventory():
    inventory = defaultdict(list)
    inventory['_meta'] = {
        'hostvars' : {},
    }
    for node in _listnodes():
        # skip deleting and offline nodes
        if node['pending_deletion'] and inventory_cfg['skip_deleting']: continue
        if not node['online'] and inventory_cfg['skip_offline']: continue

        hostname = node['name']
        [ inventory[role].append(hostname) for role in node['roles'].split(",") ]
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
    _read_config()
    inventory = fuel_inventory()
    if options.list:
        data = json.dumps(inventory)
        print data
    elif options.host:
        data = json.dumps(inventory['_meta']['hostvars'][options.host])
        print data
