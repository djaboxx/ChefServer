# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.synced_folder "./", "/opt/chef"
  config.vm.provision "shell", inline: "sudo apt-get update && sudo apt-get install -y python python-dev python-pip"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "infrastructure/playbooks/chefdk_setup.yaml"
  end
end
