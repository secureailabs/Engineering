# Secure AI Labs

## _Express Server_

The Express server is used to serve the React app and proxy API requests to hide the Eosb token from the browser.

## Setup

- Install Nodejs and npm if you haven't yet.
- Clone the Repo
- cd into /WebApp/server/src/
- Create a .env (read the following section)
- Run npm install
- Run npm start

## Create .env

- location -> Root of the application -> ./.env (ex: /WebApp/server/.env)
- Must contain the following:
  SAIL_API=<SAIL_API_ENDPOINT-(ex:"https://40.76.22.246:6200")>
  CLIENT_API=<CLIENT_API-(ex:"http://localhost:8080")>
  NODE_TLS_REJECT_UNAUTHORIZED= "0"
  NODE_ENV=<ENV-(development|production)>

## API Endpoints

The Express server (proxy-request middleware) will proxy every request from https://github.com/secureailabs/Development/blob/main/Milestone2/EndPointTools/RestPortalTester/Sources/InteractiveClient.cpp
**Example**: /SAIL/AuthenticationManager/User/Login -> /api/v1/AuthenticationManager/User/Login

- _You have to specify all the parameters you would normally include in a request to the REST Portal except the Eosb/IEosb_
- _It only accepts json parameters_
- _The server listens on port 3000_
- _Only account-related endpoints have been tested_

## Eosb Management

- When you send a Login request, the Express server will forward it to the REST Portal but the eosb-manager middleware will remove the Eosb from the response to the client. It will instead save it to your "session".
- When you make a request that require an Eosb, you don't have to include it. The eosb-manager middleware will add it for you in the request if you previously logged in.

## Production

- To run the server in production all you need to do is specify NODE_ENV=production. However, in production, the server will also host the client (react app). The server will automatically search for the build in (WebApp/client/build). Please make sure to build the client application (please check the client documentation for more information)
