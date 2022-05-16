#!/bin/bash
set -e
mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost --fork --logpath /var/log/mongod.log

cd /app || exit

uvicorn app.main:server --reload --host 0.0.0.0 --port 8000

# To keep the container running
tail -f /dev/null
