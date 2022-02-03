#!/bin/bash

cd app/sail || exit
pip3 install .
cd ..
jupyter notebook --ip=0.0.0.0 --port=8080 --allow-root 2>&1 | tee orchestrator.log
