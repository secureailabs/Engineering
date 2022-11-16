FROM ubuntu:20.04

ENV TZ=America/Toronto
USER root

# Set time zone data
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    uuid \
    nginx \
    jq \
    cifs-utils \
    python3-dev \
    python3-pip \
    python3.8-venv \
    zip

COPY nginx.conf /etc/nginx/nginx.conf

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --upgrade pip \
    && pip3 install numpy \
    && pip3 install pandas \
    && pip3 install scipy \
    && pip3 install sklearn \
    && pip3 --no-cache-dir install torch \
    && pip3 install matplotlib \
    && pip3 install fastapi \
    && pip3 install uvicorn \
    && pip3 install python-multipart \
    && pip3 install psutil \
    && pip3 install msgpack \
    && pip3 install pyzmq

RUN mkdir /ds
COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

ENTRYPOINT [ "/Entrypoint.sh" ]
CMD ["/bin/bash"]
