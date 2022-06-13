FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  jq \
  curl \
  nginx

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs  && \
  rm -rf /var/lib/apt/lists/*

RUN npm install --global yarn
RUN node --version

COPY nginx.conf /etc/nginx/nginx.conf

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

ENTRYPOINT [ "/Entrypoint.sh" ]
CMD ["/bin/bash"]
