FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y sudo \
wget \
iproute2 \
git \
make \
build-essential \
libcurl4-gnutls-dev \
python3-pip

COPY install.sh /install.sh
RUN chmod +x /install.sh
RUN /install.sh

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

EXPOSE 6200

CMD ["/bin/bash", "/Entrypoint.sh"]
