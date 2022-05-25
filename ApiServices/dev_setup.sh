# Install python3
sudo apt-get install python3

# Install python venv
sudo apt-get install python3-venv

# Create a virutal environment
python3 -m venv dev_env2

# Activate it
source dev_env2/bin/activate

# Install all the requirements
pip3 install -r requirements.txt

# Install redoc-cli for static document generation
npm install -g redoc-cli
