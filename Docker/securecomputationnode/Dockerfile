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
    zip \
    sudo

COPY securecomputationnode/requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# Install Jupyter Notebook
RUN pip3 install -U jupyter

# Install sail data layer
COPY securecomputationnode/sail_data_layer-1.0.1-py3-none-any.whl /sail_data_layer-1.0.1-py3-none-any.whl
RUN pip3 install /sail_data_layer-1.0.1-py3-none-any.whl

COPY vm-initializer/decrypt_file.py /decrypt_file.py

COPY securecomputationnode/Entrypoint.sh /Entrypoint.sh
# COPY securecomputationnode/nginx.conf /etc/nginx/nginx.conf
RUN chmod +x /Entrypoint.sh

RUN useradd -ms /bin/bash jupyternotebook
RUN echo "jupyternotebook ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/jupyternotebook

USER jupyternotebook

ENTRYPOINT [ "/Entrypoint.sh" ]
