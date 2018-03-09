# Overview

This Repository is a basic repository as what is output by "chef generate repository <name>"; however, it also comes bundled with some goodies.

## Infrastructure Setup
In the infrastructure directory, you will find Terraform Code that will create a new Chef server for you in AWS. After filling out some important variables information, you will be able to run "terraform apply" and a new ec2 instance will be spun up in a new vpc/subnet.

The Terraform code in this directory assumes you have DNS in Route53 and have DNS Zone ID. The server name will be the hostname of the machine.
The Terraform code in this directory will look for an ssh key in ~/.ssh/ that is named <key_name>.pub. This will be used as the ssh key of the newly created chef server.

	key_name="chef-server"
	server_name=""
	domain=""
	region= "us-east-1"
	subnet_cidr= "10.0.1.0/24"
	vpc_cidr= "10.0.0.0/16"
	route53_zone_id= ""

## Chef Server Configuration
In the infrastructure/playbooks directory, you will find playbooks to configure the chef-server and optionally install chef-manage (The Chef UI). 

	ansible-playbook infrastructure/playbooks/chef_setup.yaml \
	--vault-password-file=~/vault_password \
	-i ./infrastructure/playbooks/inventories/ec2.py \
	-e org=<chef_org_name> \
	-u ubuntu \
	--private-key=~/.ssh/chef-server \
	-b -e install_chef_manage=True \
	-e server_name=chef \
	-e domain_name=ops.happypathway.com \
	-e force_org=true

This playbook assumes that you have an admin user setup in infrastructure/playbooks/chef_users.yaml and that you have it password protected and are therefor using ansible-vault. The password for ansible-vault will be kept in ~/vault_password. 

The Format of the chef_users.yaml file will be similar to as follows:
	
	---
	chef_admin:
    	user: devops
    	fname: Dave
    	lname: Arnold
    	email: devops@happypathway.com
    	admin: true
    	password: testing

Every Chef installation needs a Chef Repository. This is the place where cookbooks, roles, config files and other artifacts for managing systems with Chef will live. We strongly recommend storing this repository in a version control system such as Git and treat it like source code.

While we prefer Git, and make this repository available via GitHub, you are welcome to download a tar or zip archive and use your favorite version control system to manage the code.

# Repository Directories

This repository contains several directories, and each directory contains a README file that describes what it is for in greater detail, and how to use it for managing your systems with Chef.

- `cookbooks/` - Cookbooks you download or create.
- `data_bags/` - Store data bags and items in .json in the repository.
- `roles/` - Store roles in .rb or .json in the repository.
- `environments/` - Store environments in .rb or .json in the repository.

# Configuration

The config file, `.chef/knife.rb` is a repository specific configuration file for knife. If you're using the Chef Platform, you can download one for your organization from the management console. If you're using the Open Source Chef Server, you can generate a new one with `knife configure`. For more information about configuring Knife, see the Knife documentation.

<https://docs.chef.io/knife.html>

# Next Steps

Read the README file in each of the subdirectories for more information about what goes in those directories.
