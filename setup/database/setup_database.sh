#!/bin/sh
# This script bootstraps the database box, it's designed for Debian
# NOTE: It should be ran as root

install_docker() {
    # install dependencies
    apt install apt-transport-https ca-certificates lsb-release -y

    # add pgp key
    curl https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # add docker repo
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
        >> /etc/apt/sources.list.d/docker.list

    # refresh repos and install docker engine
    apt update -y
    apt install docker-ce docker-ce-cli containerd.io -y

    # add debian user (assuming this is the used non-root user) to docker
    # group so the docker command can be ran rootlessly
    usermod -aG docker debian
}

# install some basic dependencies
apt update -y
apt install curl wget gnupg -y

# install docker
install_docker

# make docker compose file
cat << EOF > docker-compose.yml

version: '3'
services:
    redis:
        image: redis
        command: redis-server --requirepass 'very secret password'
        ports:
            - 6379:6379
        volumes:
            - $PWD/redis:/data

    postgres:
        image: postgres
        ports:
            - 5432:5432
        environment:
            POSTGRES_PASSWORD: 'yet another very secret password'
        volumes:
            - $PWD/postgres:/var/lib/postgresql

EOF

# up
docker-compose up 
