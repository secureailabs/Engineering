FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  sudo \
  libcurl4-gnutls-dev \
  libcurl4 \
  libssl-dev \
  libuuid1 \
  python3-pip && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
