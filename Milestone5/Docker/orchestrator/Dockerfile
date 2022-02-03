FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  libssl-dev \
  libcurl4-openssl-dev \
  uuid-dev \
  build-essential \
  libpython3.8 \
  python3 \
  python3-pip \
  python3-dev \
  jupyter && \
  rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy
RUN pip3 install requests numpy==1.20 pandas
RUN pip3 install sklearn
RUN pip3 install shap==0.38.1
RUN pip3 install torch --no-cache-dir
RUN pip3 install xgboost
RUN pip3 install optuna

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
