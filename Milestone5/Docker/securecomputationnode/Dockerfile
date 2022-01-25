FROM ubuntu:20.04

ENV TZ=America/Toronto
LABEL authors="prawal@secureailabs.com"
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y \
libcurl4-gnutls-dev \
libcurl4 \
libssl-dev \
libuuid1 \
python3-dev \
python3-pip

RUN pip3 install numpy scipy
RUN pip3 install pandas xgboost matplotlib shap imbalanced-learn
RUN pip3 install -U scikit-learn
RUN pip3 install ipython
RUN pip3 install torch --no-cache-dir

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
