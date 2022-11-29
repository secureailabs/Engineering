#!/bin/bash
set -e
imageName=auditserver

/app/loki-linux-amd64 -config.file=/app/loki-local-config.yaml
