FROM python:3.8

RUN apt-get update && apt-get install -y \ 
    uuid

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

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

ENTRYPOINT [ "/Entrypoint.sh" ]
CMD ["/bin/bash"]
