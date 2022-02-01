#!/bin/bash

cd /app || exit
yarn --cwd client install && yarn cache clean && yarn --cwd client build

yarn --cwd server install && yarn cache clean

chmod +x /app/env.sh

/app/env.sh && yarn --cwd /app/server prod && /bin/bash
