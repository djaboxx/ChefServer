#
# Cookbook:: consul_server
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
require 'securerandom'

node[:consul][:packages].each do |pkg_name, pkg|
	#directory "/mnt/alpha/3p/#{pkg_name}" do
	#	owner "alpha"
	#	group "eng"
	#	mode 0755
	#end
	remote_file "/tmp/#{pkg_name}" do
		source "#{pkg}"
	end
	execute "unzip /tmp/#{pkg_name}" do
		cwd "/usr/local/bin"
	end
end

node.normal['consul_server']['acl_token'] = SecureRandom.uuid

template "/etc/consul.d/consul-default.json" do
	source "consul-default.json.erb"
end

cookbook_file "/usr/local/bin/consul_join.py" do
	source "consul_join.py"
	owner "root"
	mode 0755
end

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



    

