FROM node:14.16.0 as build

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y jq && \
  rm -rf /var/lib/apt/lists/*

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
