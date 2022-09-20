FROM python:3.8

RUN apt-get update && apt-get install -y \ 
    uuid

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD ./zero/zero /app/zero
WORKDIR /app/zero

RUN pip3 install --upgrade pip \ 
    && pip3 install numpy \ 
    && pip3 install pandas \
    && pip3 install scipy \
    && pip3 --no-cache-dir install torch \
    && pip3 install matplotlib \ 
    && pip3 install .

ADD ./public_keys /app/public_keys
ADD ./private_keys /app/private_keys
COPY ./test_server.py /app
COPY ./dataframe.py /app
COPY ./series.py /app
COPY ./custom_typing.py /app

WORKDIR /app
ENV port_number 5556
EXPOSE ${port_number}
CMD python ./test_server.py ${port_number}
