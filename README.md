Dynamic Ansible inventory script for Fuel managed nodes

The inventory script will group nodes into the same groups as Fuel: *controller*, *compute*, *ceph-osd*, *zabbix-server*.

If no `fuel.ini` file exists, default to include all nodes. The hipped `fuel.ini` file shows how to configure excluding offline and deleting nodes from inventory.
