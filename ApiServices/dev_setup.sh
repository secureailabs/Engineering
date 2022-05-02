# Install python3.10
sudo apt-get install python3.10

# Install python venv
sudo apt-get install python3.10-venv

# Create a virutal environment
python3.10 -m venv dev_env

# Activate it
source dev_env/bin/activate

# Install all the requirements
pip3 install -r requirements.txt

# Install redoc-cli for static document generation
npm install -g redoc-cli
