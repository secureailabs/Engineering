FROM node:14.16.0 as build

COPY Entrypoint.sh /Entrypoint.sh
RUN chmod +x /Entrypoint.sh

CMD ["/bin/bash", "/Entrypoint.sh"]
