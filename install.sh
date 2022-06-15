#!/bin/sh

echo "Installing required packages"

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

echo "Installation complete!"
