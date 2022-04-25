# Import public key
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Update the package index files
apt-get update

# Install the latest version of MongoDB
apt-get install -y mongodb-org

# Pin the packages at the currently installed versions
echo "mongodb-org hold" | dpkg --set-selections
echo "mongodb-org-server hold" | dpkg --set-selections
echo "mongodb-org-shell hold" | dpkg --set-selections
echo "mongodb-org-mongos hold" | dpkg --set-selections
echo "mongodb-org-tools hold" | dpkg --set-selections

systemctl daemon-reload
# Start MongoDB
systemctl start mongod

mkdir -p /srv/mongodb/db0
chown -R mongodb:mongodb /srv/mongodb/db0
mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost --fork --logpath /var/log/mongod.log
mongo --eval "rs.initiate()"
