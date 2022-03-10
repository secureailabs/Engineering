FROM nginx:latest

WORKDIR /app
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY Entrypoint.sh .
RUN chmod +x Entrypoint.sh

CMD ["bash","Entrypoint.sh"]
