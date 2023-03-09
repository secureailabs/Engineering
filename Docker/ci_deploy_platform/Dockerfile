# Engineering
# Dockerfile
# 
# Copyright (C) 2023 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
# 
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# 
# 
FROM ubuntu:20.04
ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Base Dependencies
RUN apt-get update && apt-get -y upgrade && apt-get install -y\
    git \
    wget \
    curl \
    sudo \
    python3-pip \
    docker.io

# Install dotnet
RUN wget https://dot.net/v1/dotnet-install.sh
RUN chmod +x ./dotnet-install.sh
RUN ./dotnet-install.sh --version latest

# Install python dependencies
COPY ci_deploy_platform/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Install azure cli
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash