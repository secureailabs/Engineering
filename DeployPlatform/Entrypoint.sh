#!/bin/bash
set -e
set -x

cd /app

source deploy_config.sh
python3 Deploy.py
