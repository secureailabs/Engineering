#!/bin/bash

#package necessary files and dirs
tar -zcvf auditserver.tar.gz cert.pem client.pem server.pem loki-linux-amd64 loki-local-config.yaml

#move the package to Binary
mv ./auditserver.tar.gz ../Binary/
