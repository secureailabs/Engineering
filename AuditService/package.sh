#!/bin/bash

#package necessary files and dirs
tar -zcvf auditserver.tar.gz loki_linux_amd64 loki_local_config.yaml

#move the package to Binary
mv ./auditserver.tar.gz ../Binary/