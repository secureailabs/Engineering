FROM node:14.16.0 as build

WORKDIR /app

COPY Entrypoint.sh /app/Entrypoint.sh
RUN chmod +x /app/Entrypoint.sh

EXPOSE 3000

CMD ["/app/Entrypoint.sh"]
