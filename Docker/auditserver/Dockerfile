FROM ubuntu:20.04

ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y

COPY loki-linux-amd64 /app/loki-linux-amd64
COPY loki-local-config.yaml /app/loki-local-config.yaml

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

ENTRYPOINT [ "/Entrypoint.sh" ]
