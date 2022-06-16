# Install python3
sudo apt-get install python3

# Install python venv
sudo apt-get install python3-venv

# Create a virutal environment
python3 -m venv venv38-sail_test

# Activate it
source venv38-sail_test/bin/activate

# Install all the requirements
pip3 install -r config/requirements/all_requirements.txt

# Install redoc-cli for static document generation
curl -fsSL https://deb.nodesource.com/setup_current.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g redoc-cli
