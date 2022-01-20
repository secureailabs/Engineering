SAIL client

## MAKE SURE TO START THE NODE SERVER BEFORE STARTING THE CLIENT

    # Please check ScratchPad/VincentQuirion/WebApp/server

## FIRST TIME INSTALL

# Create a .env (location: .env (ex: ScratchPad/VincentQuirion/WebApp/client/.env)):

SNOWPACK_PUBLIC_API_URL_DEV=<NODE_SERVER_URL-(ex: "http://localhost:3000")>

# Run the following commands:

yarn install

## START THE SERVER (DEV)

yarn dev

## BUILD THE SERVER

yarn build

# The server needs to be built in order to be ran in production (the node-server takes care of servering it)
