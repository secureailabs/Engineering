from fastapi import FastAPI
from app.api import authentication, datasets, users, digitalcontracts, organization, scn

server = FastAPI()

server.include_router(organization.router)
server.include_router(users.router)
server.include_router(authentication.router)
server.include_router(datasets.router)
server.include_router(digitalcontracts.router)
server.include_router(scn.router)
