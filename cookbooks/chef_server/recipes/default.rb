#
# Cookbook:: chef_server
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.
chef_user = data_bag_item("credentials", "chef-server", IO.read(node[:encrypted_data_bag_secret_path]))

chef_org = node[:chef_server][:org]

#directory chef_user[:key_dir] do
#	recursive true
#end

apt_package "python-pip"

cookbook_file "/tmp/requirements.txt" do
	source "requirements.txt"
end

execute "pip install -r /tmp/requirements.txt"

remote_file "/tmp/#{node[:chef_package]}" do
	source "https://s3.amazonaws.com/happypathway-public-assets/chef/chef-server-core_12.17.33-1_amd64.deb"
end

dpkg_package "chef" do
	source "/tmp/#{node[:chef_package]}"
end

directory "/opt/chef/cookbooks"
file "/etc/opscode/chef-server.rb" do
	content "nginx['enable_non_ssl'] = true"
end

execute "chef-server-ctl reconfigure"


#directory "/root/.chef"
#execute "chef-server-ctl user-create #{chef_user[:username]} #{chef_user[:full_name]} #{chef_user[:email]} '#{chef_user[:password]}' --filename /root/.chef/#{chef_user[:username]}.pem"
#execute "chef-server-ctl org-create #{chef_org[:short_name]} '#{chef_org[:full_name]}' --association_user #{chef_user[:username]} --filename /root/.chef/#{chef_org[:short_name]}-validator.pem"

#template "/root/.chef/knife.rb" do
#	source "knife.rb.erb"
#	variables({
#		key_name: "#{chef_user[:username]}.pem",
#		node_name: chef_user[:username]
#		})
#end

#file "/tmp/#{node[:chef_package]}" do
#	action :delete
#end

#   
# execute "knife ssl fetch"
execute "mv /etc/chef/* /root/.chef/"