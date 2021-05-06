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

install_java() {
    wget https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u292-b10_openj9-0.26.0/OpenJDK8U-jdk_x64_linux_openj9_8u292b10_openj9-0.26.0.tar.gz
    tar xf OpenJDK*.tar.gz
    rm OpenJDK*.tar.gz
    echo "export PATH=$(pwd)/jdk8u292-b10/bin:\$PATH" >> ~/.bashrc
    . ~/.bashrc

    sudo apt install maven -y
}

build_dockerizedcraft() {
    cd /mnt/data

    sudo git clone https://github.com/DockerizedCraft/Core DockerizedCraft
    cd DockerizedCraft

    sudo MAVEN_OPTS='-Dmaven.repo.local=/mnt/data/.m2' mvn package
    sudo mv target/DockerizedCraft*.jar ../plugins/DockerizedCraft.jar
}

build_image()  {
    cd ~/infrastructure/setup/craft/images/$1
    docker build . -t $1
}

# install some basic dependencies
sudo apt update -y
sudo apt install git curl wget gnupg -y

# mount data volume to /mnt/data
sudo mkdir -p /mnt/data
sudo mount /dev/vdb1 /mnt/data
sudo mkdir -p /mnt/data/plugins

# install docker and java
install_docker
install_java

# build dockerizedcraft
build_dockerizedcraft

# build docker images
build_image lobby

# make docker compose file
cat << EOF > docker-compose.yml
version: '3'
services:
    bungeecord:
        image: itzg/bungeecord
        environment:
            - UID=1000
        ports:
            - 25565:25577
        volumes:
            - /mnt/data/plugins/DockerizedCraft.jar:/server/plugins/DockerizedCraft.jar
            - //var/run/docker.sock:/var/run/docker.sock
        networks:
            - local

networks:
    local:
EOF

# up
sudo docker-compose -f ./docker-compose.yml up
