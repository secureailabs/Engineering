#!/bin/bash

export AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID
export AZURE_TENANT_ID=$AZURE_TENANT_ID
export AZURE_CLIENT_ID=$AZURE_CLIENT_ID
export AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET
export AZURE_OBJECT_ID=$AZURE_OBJECT_ID
export SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL
export DOCKER_REGISTRY_URL=$DOCKER_REGISTRY_URL
export DOCKER_REGISTRY_USERNAME=$DOCKER_REGISTRY_USERNAME
export DOCKER_REGISTRY_PASSWORD=$DOCKER_REGISTRY_PASSWORD

# this is a hack to let the CI use default values for the tags
# the CI will override the $ values with the user provided tags
# if the user does not provide any tags, the default values will be used
export API_SERVICES_TAG="v0.1.0_19e39ff"
export API_SERVICES_TAG=$API_SERVICES_TAG
export AUDIT_SERVICES_TAG="v0.1.0_d1dae58b"
export AUDIT_SERVICES_TAG=$AUDIT_SERVICES_TAG
export AGGREGATOR_SCN_TAG="v0.1.0_ae9c6c0b"
export AGGREGATOR_SCN_TAG=$AGGREGATOR_SCN_TAG
export PARTICIPANT_SCN_TAG="v0.1.0_ae9c6c0b"
export PARTICIPANT_SCN_TAG=$PARTICIPANT_SCN_TAG
export WEB_FRONTEND_TAG="v0.1.0_d1dae58b"
export WEB_FRONTEND_TAG=$WEB_FRONTEND_TAG
