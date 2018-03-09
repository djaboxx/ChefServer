#!/usr/bin/env python
import os
from subprocess import Popen, PIPE
import subprocess
import re
import sys
import json

def sync_roles(role_dir):
    print "Syncing roles..."
    role_list = Popen("knife role list", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = role_list.communicate()
    for x in out.splitlines():
        print "syncing {0}...".format(x)
        role = Popen("knife role show -Fjson {0}".format(x), shell=True, stdout=PIPE, stderr=PIPE)
        role_out, role_err = role.communicate()
        with open(os.path.join(role_dir, "{0}.json".format(x)), "w") as role_file:
            role_file.write(json.dumps(json.loads(role_out), separators=(',',':'), indent=4, sort_keys=True))
    

def sync_envs(env_dir):
    print "Syncing Environments..."
    env_list = Popen("knife environment list", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = env_list.communicate()
    for x in out.splitlines():
        print "syncing {0}...".format(x)
        env = Popen("knife environment show -Fjson {0}".format(x), shell=True, stdout=PIPE, stderr=PIPE)
        env_out, env_err = env.communicate()
        with open(os.path.join(env_dir, "{0}.json".format(x)), "w") as env_file:
            env_file.write(json.dumps(json.loads(env_out), separators=(',',':'), indent=4, sort_keys=True))


def sync_nodes(node_dir):
    print "Syncing nodes..."
    node_list = Popen("knife node list", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = node_list.communicate()
    for x in out.splitlines():
        print "syncing {0}...".format(x)
        node = Popen("knife node show -Fjson {0}".format(x), shell=True, stdout=PIPE, stderr=PIPE)
        node_out, node_err = node.communicate()
        with open(os.path.join(node_dir, "{0}.json".format(x)), "w") as node_file:
            node_file.write(json.dumps(json.loads(node_out), separators=(',',':'), indent=4, sort_keys=True))


def sync_clients(client_dir):
    print "Syncing clients..."
    client_list = Popen("knife client list", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = client_list.communicate()
    for x in out.splitlines():
        print "syncing {0}...".format(x)
        client = Popen("knife client show -Fjson {0}".format(x), shell=True, stdout=PIPE, stderr=PIPE)
        client_out, client_err = client.communicate()
        with open(os.path.join(client_dir, "{0}.json".format(x)), "w") as client_file:
            client_file.write(json.dumps(json.loads(client_out), separators=(',',':'), indent=4, sort_keys=True))


def sync_databags(data_bag_dir):
    print "Syncing DataBags..."
    data_bag_list = Popen("knife data bag list", shell=True, stdout=PIPE, stderr=PIPE)
    data_bag_list_out, err = data_bag_list.communicate()
    for bag in data_bag_list_out.splitlines():
        data_bag_items = Popen("knife data bag show {0}".format(bag), shell=True, stdout=PIPE, stderr=PIPE)
        data_bag_items_out, node_err = data_bag_items.communicate()
        for item in data_bag_items_out.splitlines():
            print "syncing {0}:{1}...".format(bag, item)
            data_bag_contents = Popen("knife data bag show -Fjson {0} {1}".format(bag, item), shell=True, stdout=PIPE, stderr=PIPE)
            data_bag_contents_out, data_bag_contents_err = data_bag_contents.communicate()
            _data_bag_dir = os.path.join(data_bag_dir, bag)
            print _data_bag_dir
            if not os.path.isdir(_data_bag_dir):
                os.mkdir(_data_bag_dir)
            with open(os.path.join(_data_bag_dir, "{0}.json".format(item)), "w") as data_bag_file:
                print data_bag_file.name
                data_bag_file.write(json.dumps(json.loads(data_bag_contents_out), separators=(',',':'), indent=4, sort_keys=True))


def sync_cookbooks(cookbook_dir):
    # for cookbook in $(knife cookbook list | awk '{ print $1 }'); do knife cookbook show ${cookbook}; done
    print "Syncing cookbooks..."
    cb_list = Popen("knife cookbook list", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = cb_list.communicate()
    for x in out.splitlines():
        cb_name = x.split()[0]
        print "syncing {0}...".format(x)
        cb = Popen("knife cookbook show {0}".format(cb_name), shell=True, stdout=PIPE, stderr=PIPE)
        cb_out, cb_err = cb.communicate()
        cb_versions = cb_out.split()[1:]
        for version in cb_versions:
            if force:
                cbdl_v = Popen("knife cookbook download --force --dir={0} {1} {2}".format(cookbook_dir, cb_name, version), shell=True, stdout=PIPE, stderr=PIPE)
            else:
                cbdl_v = Popen("knife cookbook download --dir={0} {1} {2}".format(cookbook_dir, cb_name, version), shell=True, stdout=PIPE, stderr=PIPE)
            cbdl_v_out, cbdl_v_err = cbdl_v.communicate()
            print cbdl_v_out
            print cbdl_v_err

def main(opt, args):
    if 'roles' in args:
        sync_roles(opt.roles)
    if 'nodes' in args:
        sync_nodes(opt.nodes)
    if 'clients' in args:
        sync_clients(opt.clients)
    if 'envs' in args:
        sync_envs(opt.envs)
    if 'data_bags' in args:
        sync_databags(opt.dbags)
    if 'cookbooks' in args:
        sync_cookbooks(opt.cookbooks)

def get_path(item):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../{0}'.format(item))

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--roles', default=get_path('roles'))
    parser.add_option('--nodes', default=get_path('nodes'))
    parser.add_option('--clients', default=get_path('clients'))
    parser.add_option('--envs', default=get_path('environments'))
    parser.add_option('--cookbooks', default=get_path('cookbooks/releases'))
    parser.add_option('--dbags', default=get_path('data_bags'))
    parser.add_option('--force', default=False, action='store_true', help="used with syncing cookbooks, will overwrite release dir if applied")
    opt, args = parser.parse_args()
    main(opt, args)

