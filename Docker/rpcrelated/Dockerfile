FROM ubuntu:20.04

ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    uuid \
    nginx \
    jq \
    iputils-ping \
    unzip \
    cifs-utils \
    python3-dev \
    python3-pip \
    python3.8-venv \
    zip

COPY rpcrelated/nginx.conf /etc/nginx/nginx.conf

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY rpcrelated/requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY datascience /datascience
WORKDIR /datascience/sail-core
RUN pip3 install -e /datascience/sail-core
WORKDIR /datascience/sail-safe-functions
RUN pip3 install -e /datascience/sail-safe-functions

RUN useradd --system promtail

COPY rpcrelated/Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

COPY vm-initializer/vm_initializer.py /vm_initializer.py

ENTRYPOINT [ "/Entrypoint.sh" ]
