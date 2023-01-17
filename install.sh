#!/bin/sh

echo "Installing required packages"

sudo apt-get install -y python3-pip

# Install required python packages
pip3 install poetry==1.2.2

echo "Installation complete!"
