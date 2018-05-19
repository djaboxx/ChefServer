#!/usr/bin/env python
import boto
import requests
from boto import ec2
import subprocess
import json

class ConsulNode(object):

    def __init__(self):
        self._instance_id = None
        self._tags = None
        self._servers = None
        resp = requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone").text[0:-1]
        self.e_conn = ec2.connect_to_region(resp)
        resp = requests.get("http://169.254.169.254/latest/meta-data/instance-id").text
        self.instance_id = resp
        instance = self.e_conn.get_only_instances([self.instance_id]).pop()
        self.instance = instance
        self.tags = instance.tags
        print self.tags

    @property
    def consul_server(self):
        if self.tags.get("consul") == "Server":
            return True
        else:
            return False

    @property
    def consul_agent(self):
        if self.tags.get("consul") == "Agent":
            return True
        else:
            return False

    @property
    def servers(self):
        if not self._servers:
            f = {'tag:ConsulDC': self.tags.get('ConsulDC'), 'tag:consul': 'Server'}
            self._servers = self.e_conn.get_only_instances(filters=f)
            return self._servers
        else:
            return self._servers

    def set_node_attrs(self):
        my_ip = [x.ip_address for x in self.servers if x.tags.get("Name") == self.tags.get("Name")].pop()
        with open("/etc/consul.d/consul-default.json", "r") as _consul_config:
            self.consul_config = json.loads(_consul_config.read())
        self.consul_config["advertise_addr"] = my_ip
        self.consul_config["node_name"] = self.tags.get("Name")
        self.consul_config["datacenter"] = self.tags.get("ConsulDC")
        self.consul_config["acl_datacenter"] = self.tags.get("ConsulDC")
        retry = "provider=aws tag_key=ConsulDC tag_value={0} region={1}".format(
                                                                            self.tags.get("ConsulDC"), 
                                                                            self.instance.region.name
                                                                        )
        self.consul_config["retry_join"] = [retry]
        with open("/etc/consul.d/consul-default.json", "w") as _consul_config:
            _consul_config.write(json.dumps(self.consul_config, separators=(',', ':'), indent=4, sort_keys=True))
            

    @property
    def cluster_init(self):
        if len(self.servers) >= 0:
            return True
        else:
            return False

    def force_leave(self):
        p = subprocess.Popen("consul force-leave {0}".format(self.tags.get('Name')), 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            print str(err)
        else:
            print str(out)

    def restart(self):
        p = subprocess.Popen(
            "supervisorctl restart consul", 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode > 0:
            return False
        else: 
            return True

    def join(self):
        cmd = "consul join {0}:8301"
        for x in self.servers:
            if x.private_ip_address == self.instance.private_ip_address:
                continue
            cmd = cmd.format(x.private_ip_address)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if err:
                print str(err)
            else:
                print str(out)

def main():
    node = ConsulNode()
    node.set_node_attrs()
    if node.restart():
        node.join()
    else:
        print "Could not restart Consul service"

if __name__ == '__main__':
    main()
