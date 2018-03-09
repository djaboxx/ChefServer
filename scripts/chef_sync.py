#!/usr/bin/env python
import os
from subprocess import Popen, PIPE
import subprocess
import re
import sys


def sync_roles(commit_msg):
    roles_regex = re.compile("chef-role:(?P<role>[^\s]*)")
    m = roles_regex.search(commit_msg)
    if m.group('role'):
        cmd = "knife role from file roles/{0}.json".format(m.group("role"))
        print cmd
        p = subprocess.Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        out, err = p.communicate()
        if len(err):
            sys.stderr.write(err)
            sys.stderr.flush()

def sync_envs(commit_msg):
    envs_regex = re.compile("chef-env[ironment]*:(?P<env>[^\s]*)")
    m = envs_regex.search(commit_msg)
    if m.group('env'):
        cmd = "knife environment from file environments/{0}.json".format(m.group("env"))
        print cmd
        p = subprocess.Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        out, err = p.communicate()
        if len(err):
            sys.stderr.write(err)
            sys.stderr.flush()

def sync_cookbooks(commit_msg):
    cookbooks_regex = re.compile("chef-cookbook:(?P<cookbook>[^\s]*)")
    m = cookbooks_regex.search(commit_msg)
    if m.group('cookbook'):
        ret = os.system("knife cookbook test {0}".format(m.group("cookbook")))
        if ret != 0:
            return 1
        cmd = "knife cookbook upload {0}".format(m.group("cookbook"))
        print cmd
        p = subprocess.Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        out, err = p.communicate()
        if len(err):
            sys.stderr.write(err)
            sys.stderr.flush()

def sync_nodes(commit_msg):
    nodes_regex = re.compile("chef-node:(?P<node>[^\s]*)")
    m = nodes_regex.search(commit_msg)
    if m.group('node'):
        cmd = "knife node from file nodes/{0}.json".format(m.group("node"))
        print cmd
        p = subprocess.Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        out, err = p.communicate()
        if len(err):
            sys.stderr.write(err)
            sys.stderr.flush()


def main():
    try:
        p = Popen("git log --format=%B -n 1 {0}".format(os.environ.get('GIT_COMMIT')), shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print line
            if "chef-node" in line:
                sync_nodes(line)
            if "chef-cookbook" in line:
                sync_cookbooks(line)
            if "chef-env" in line:
                sync_envs(line)
            if "chef-role" in line:
                sync_roles(line)

    except Exception, e:
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()

