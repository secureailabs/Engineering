#!/bin/bash

set -e

npx senv encrypt .env.dev > .env.dev.encrypted
