FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  jq \
  curl \
  nginx \
  python3 \
  python3-pip

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs  && \
  rm -rf /var/lib/apt/lists/*

RUN npm install --global yarn
RUN node --version

COPY newwebfrontend/nginx.conf /etc/nginx/nginx.conf

COPY newwebfrontend/requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY newwebfrontend/Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

COPY vm-initializer/vm_initializer.py /vm_initializer.py

ENTRYPOINT [ "/Entrypoint.sh" ]
