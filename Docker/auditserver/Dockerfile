FROM ubuntu:20.04

ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    wget \
    jq

RUN wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq && chmod +x /usr/bin/yq

COPY auditserver/InitializationVector.json /app/InitializationVector.json
COPY auditserver/loki_linux_amd64 /app/loki_linux_amd64
COPY auditserver/loki_local_config.yaml /app/loki_local_config.yaml

COPY auditserver/Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh
ENTRYPOINT [ "/Entrypoint.sh" ]
