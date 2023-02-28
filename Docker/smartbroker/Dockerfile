FROM ubuntu:20.04
ENV TZ=America/Toronto
LABEL authors="adam.hall@secureailabs.com"
USER root

# Set tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  nginx \
  wget \
  curl \
  sudo \
  build-essential \
  python3-pip \
  jq \
  iputils-ping

RUN rm -rf /var/lib/apt/lists/*

COPY smartbroker/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY datascience /datascience
WORKDIR /datascience/sail-core
RUN pip3 install -e /datascience/sail-core
WORKDIR /datascience/sail-safe-functions
RUN pip3 install -e /datascience/sail-safe-functions

COPY smartbroker/nginx.conf /etc/nginx/nginx.conf

RUN useradd --system promtail
COPY smartbroker/promtail_local_config.yaml /promtail_local_config.yaml
COPY apiservices/promtail_linux_amd64 /promtail_linux_amd64

COPY smartbroker/Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

COPY vm-initializer/vm_initializer.py /vm_initializer.py

ENTRYPOINT [ "/Entrypoint.sh" ]
