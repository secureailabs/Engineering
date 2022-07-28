#!/bin/bash

set -e

npx senv decrypt .env.dev.encrypted > .env.dev
