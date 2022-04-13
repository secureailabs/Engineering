#!/bin/bash
cd app || exit
pip3 install .
jupyter notebook --ip=0.0.0.0 --port=8080 --allow-root 2>&1 | tee orchestrator.log
