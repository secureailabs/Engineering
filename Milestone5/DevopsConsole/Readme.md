# Devops Console
This is a primary and scalable option for the devops console where one can add as many services as they want.
All the plugins can run independently and without the need of any other service but they will all be plain http.

## Run the test devops console
```
./RunDevops.sh
```
To test open the following URL in your browser:
https://localhost:8080/SamplePlugin/Hello

Accept the self-signed certificate and you must see the following message on the browser:
```
Hello from SamplePlugin
```

## Add a new plugin
### Create a new plugin
1. Create a new folder in the plugins folder with the name of the plugin.
2. Write an plugin that is a plain http server accepting REST API requests.

### Add the plugin to the devops console
1. Append the Entrypoint.sh to run the plugin independently on a unique port that has not been used by any other plugin.
2. Add a new location in the nginx/default.conf file in the format:
```
location /<Plugin Name> {
    proxy_pass http://127.0.0.1:<unique_plugin_port>;
}
```

## Create self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt

## TODO
- Add more plugins
- Each plugin can have its own docker container
- Add real certificates
- Add a self deploy script
- Create an Azure VM image to run this
- Add authentication at the nginx level
- Run it on 443 instead of 8080
- Run the production version of flask
- Deploy best practices from https://www.cyberciti.biz/tips/linux-unix-bsd-nginx-webserver-security.html
- Add a version of everything in the docker files
