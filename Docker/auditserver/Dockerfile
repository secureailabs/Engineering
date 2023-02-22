FROM ubuntu:20.04

ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    nginx \
    python3-pip \
    wget \
    jq

RUN wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq && chmod +x /usr/bin/yq

COPY auditserver/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY auditserver/nginx.conf /etc/nginx/nginx.conf

COPY auditserver/Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

COPY vm-initializer/vm_initializer.py /vm_initializer.py

ENTRYPOINT [ "/Entrypoint.sh" ]
