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
  wget \
  curl \
  sudo \
  build-essential \
  python3-pip

RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY install.sh /install.sh
RUN chmod +x /install.sh && /install.sh

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
