FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
USER root
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y \
  libcurl4-gnutls-dev \
  libcurl4 \
  libssl-dev \
  nginx \
  libuuid1 \
  python3-dev \
  python3-pip && \
  rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy scipy pandas xgboost matplotlib shap imbalanced-learn ipython
RUN pip3 install -U scikit-learn
RUN pip3 install torch --no-cache-dir

COPY nginx.conf /etc/nginx/nginx.conf

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
