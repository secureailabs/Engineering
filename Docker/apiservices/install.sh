#!/bin/sh

# Update the package index files
sudo apt-get update
# Run Upgrade
sudo apt-get -y upgrade

# Install required packages
sudo apt-get install -y build-essential
sudo apt-get install -y cmake
sudo apt-get install -y libssl-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y curl
# Required for Guid
sudo apt-get install -y uuid-dev
sudo apt-get install -y libcurl3-gnutls libcurl4-openssl-dev

echo "Installing MongoDB"

# Import public key
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Update the package index files
sudo apt-get update

# Install the latest version of MongoDB
sudo apt-get install -y mongodb-org

# Pin the packages at the currently installed versions
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

sudo systemctl daemon-reload
# Start MongoDB
sudo systemctl start mongod

# Stop mongod
sudo systemctl stop mongod

# Deploy a replica set
sudo mkdir -p /srv/mongodb/db0
sudo chown -R mongodb:mongodb /srv/mongodb/db0
sudo mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost --fork --logpath /var/log/mongod.log
mongo --eval "rs.initiate()"


curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

echo "Installation complete!"
