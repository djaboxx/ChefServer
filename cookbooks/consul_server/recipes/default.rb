#
# Cookbook:: consul_server
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
require 'securerandom'

apt_package "unzip"
node[:consul][:packages].each do |pkg|
	remote_file "/tmp/#{pkg[:pkg_name]}" do
		source "#{pkg[:pkg]}"
	end
	execute "unzip /tmp/#{pkg[:pkg_name]}" do
		cwd "/usr/local/bin"
	end
end

node.normal['consul_server']['acl_token'] = SecureRandom.uuid

directory "/etc/consul.d"
template "/etc/consul.d/consul-default.json" do
	source "consul-default.json.erb"
end

cookbook_file "/usr/local/bin/consul_join.py" do
	source "consul_join.py"
	owner "root"
	mode 0755
end

directory "/etc/vault"
cookbook_file "/etc/vault/vault.conf" do
	source "vault.conf"
end

apt_package "supervisor"
supervisord_configs = ["consul", "vault"]
supervisord_configs.each do |config|
	cookbook_file "/etc/supervisor/conf.d/#{config}.conf" do
		source "supervisord_#{config}.conf"
	end
end

service "supervisor" do
	action :enable
end

execute "echo /usr/local/bin/consul_join.py >> /etc/rc.local"