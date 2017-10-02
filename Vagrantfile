# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/ubuntu-16.04"

  config.vm.network "private_network", ip: "10.0.22.5"
  config.vm.hostname = "longview-backend"

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
    vb.gui = false
  
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
  end
 
  config.vm.provision "shell", inline: <<-SHELL
     timedatectl set-timezone Europe/Berlin    
     sudo apt-get update
     sudo apt-get install -y git
  SHELL
end
