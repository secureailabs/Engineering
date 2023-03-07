FROM ubuntu:20.04

ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    nginx \
    jq \
    unzip \
    python3-pip \
    python3.8-venv \
    cifs-utils \
    zip

COPY securecomputationnode/nginx.conf /etc/nginx/nginx.conf

COPY securecomputationnode/requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# Install Jupyter Notebook
RUN pip3 install -U jupyter

COPY vm-initializer/vm_initializer.py /vm_initializer.py
COPY vm-initializer/decrypt_file.py /decrypt_file.py

COPY securecomputationnode/Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

ENTRYPOINT [ "/Entrypoint.sh" ]
