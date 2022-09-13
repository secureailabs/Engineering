FROM ubuntu:18.04
FROM python:3

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y uuid
RUN apt-get install -y python3-pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scipy
RUN pip3 install torch
RUN pip3 install matplotlib

ADD ./zero/zero /app/zero
WORKDIR /app/zero
RUN pip3 install .

ADD ./public_keys /app/public_keys
ADD ./private_keys /app/private_keys

COPY ./test_server.py /app
COPY ./dataframe.py /app
COPY ./series.py /app
COPY ./custom_typing.py /app
WORKDIR /app
ENV port_number 5556
EXPOSE ${port_number}
CMD python3 ./test_server.py ${port_number}
