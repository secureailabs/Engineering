#!/bin/bash

cd /app
mongod --port 27017 --dbpath /srv/mongodb/db0 --replSet rs0 --bind_ip localhost --fork --logpath /var/log/mongod.log
./DatabaseGateway 2>&1 | tee databasegateway.log &
./RestApiPortal 2>&1 | tee restportal.log &
tail -f /dev/null
