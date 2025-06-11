#!/bin/bash

####
#
#   Debian
#
####

## Install dependencies
# sudo apt-get update
# sudo apt-get upgrade -y
sudo apt-get install -y git ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update



# Install docker latest version
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

if [[ -z ~/post-app ]]; then
  ## Clone flask app repository
  mkdir ~/post-app && cd ~/post-app
  git clone https://github.com/kieukhang185/post_app.git .
else
  cd ~/post-app
fi
# https://github.com/kieukhang185/post_app.git
# git clone https://github.com/kieukhang185/post_app.git .

# Change docker permission
sudo chmod 666 /var/run/docker.sock
sudo systemctl restart docker.service

## Deploy Flask app wit docker compose
# docker-compose pull
docker compose up -d
