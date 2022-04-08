FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  sudo \
  wget \
  iproute2 \
  git \
  make \
  build-essential \
  libcurl4-gnutls-dev \
  python3-pip && \
  rm -rf /var/lib/apt/lists/*

COPY install.sh /install.sh
RUN chmod +x /install.sh && /install.sh

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

RUN apt-get update && \
  apt-get install -y \
  nginx

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/bin/bash", "/Entrypoint.sh"]
