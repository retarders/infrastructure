#!/bin/sh
# This script sets up debian boxes with le craft
# Note: must be ran as a regular user


install_docker() {
    # install dependencies
    sudo apt install apt-transport-https ca-certificates lsb-release -y

    # add pgp key
    curl https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # add docker repo
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
        | sudo tee /etc/apt/sources.list.d/docker.list

    # refresh repos and install docker engine
    sudo apt update -y
    sudo apt install docker-ce docker-ce-cli docker-compose containerd.io -y
}

build_dockerizedcraft() {
    git clone https://github.com/DockerizedCraft/Core DockerizedCraft
    cd DockerizedCraft

    sudo apt install openjdk-8-jdk maven
    sudo maven package
}

# mount data volume to /mnt/data
sudo mkdir -p /mnt/data
sudo mount /dev/vdb /mnt/data

# install some basic dependencies
sudo apt update -y
sudo apt install git curl wget gnupg -y

# install docker
install_docker

# build dockerizedcraft
build_dockerizedcraft
