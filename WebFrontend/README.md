# README

##SAIL WEB PORTAL
#Requirements

- Node@14.16.X or higher
- Ubuntu Install:
- curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
  sudo apt-get install -y nodejs
- Yarn@1.22.X
- curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
- echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt
  sources.list.d/yarn.list
- sudo apt update
- sudo apt install yarn
- You can also use NVM to install node: https://heynode.com/tutorial/install-nodejs
  locally-nvm/
  #Setup
- First time setup:
- On the very first run, you need to install the node modules, this can easily be done
  by going to the server AND client directory and simply running
  yarn install
  #ENV variables
  The following env variables need to be applied:
  client:
- VITE_PUBLIC_API_URL: <server api_url ex: http://localhost:3000>
  server:
- SAIL_API=<sail API ex: https://52.150.26.47:6200>
- CLIENT=<for security reasons, we only want to allow connections from a specific
  client, specify the url of the client ex: http://localhost:3001>
- NODE_TLS_REJECT_UNAUTHORIZED="0"
- NODE_ENV=<development|production>

* NOTE: you don't need to use the local server if you are only developing client code.
  This means that you can use a completely external API_URL
  #Running in local env

- To run the client and the backend code in your local environnment (suited fordevelopment), ensure that you have correctly setup your environnement variables.
  Afterwards, in both the client and server directory, run "yarn dev". This will start the
  application

# Technologies being used

- Client: - Sass/Scss: We are using sass/scss for our styles. For the unfamiliar,
  - sass/scss is simply a superset/extension of css. It allows to write css in a much more organized and feature rich manor companed to regular css.
  - React: React is the framework/ui-library that is responsible for handling all of the logic. I will not dive into what react is as you have google for that.But it was chosen due to its popularity, speed and modularity.
  - Redux (we are currently migrating away from it): Redux is responsible for all of the global state managment (in our case fetching data from the API). At first we chose redux as it was an industry standard and an extremely robust solution. However, throughout development we have found that redux takes a lot of manualsetup and boiler plate compared to other pre-built solutions (react query)
  - React query: React query is a new age global state management solution. It is packed full of features that we don't need to write ourselves (caching, infinite scroll ...etc) and is actively supported. It also allows to handle our global state with much less code (no need for actions, resolvers, sagas ...etc).
  - vite: is the frontend build tool we use. It is responsible for hosting our dev server as well as compiling our frontend code to be production ready.
  - chart.js: used to render the frontend charts

# TODO

- node-sass has been deprecated in favor of dart sass (yarn add sass)
- completely get rid of redux in favour of react query (for example, users are still
  handled through react redux)
- write tests (we have no tests)
- use renovate (https://github.com/renovatebot/renovate)

## Update the IPAddresses in the client env

1. Open `client/.env`
2. Change `SNOWPACK_PUBLIC_API_URL_PROD=https://127.0.0.1:3000` to `SNOWPACK_PUBLIC_API_URL_PROD=https://<frontend_IP>:3000` where `frontend_IP` is the IP which will be used to access the WebApp

## Update the IP Addresses in the server

1. Open `server/.env`
2. Change `SAIL_API=https://backend:6200` to `SAIL_API=https://<SAIL_RestApiPortal>:6200` where `SAIL_RestApiPortal` is the public facing IP of the SAIL RestApiPortal. Note that `backend` is the domainame of the docker container which is running the SAIL RestApiPortal. But this is only applicable when both the WebApp container and the RestApiPortal container are running on the same machine.
3. Change `CLIENT=https://127.0.0.1:3000` to `CLIENT=https://<frontend_IP>:3000` where `frontend_IP` is the IP which will be used to access the WebApp

## Open the WebApp in the browser

Use the link if hosted on 127.0.0.1: https://127.0.0.1:3000/login
This won't work if localhost is used instead of 127.0.0.1

## Stop the container

If the container was started in a detached mode, use the following command to stop it:

```
docker stop $(docker ps -q --filter ancestor=frontend)
```
