from fastapi import FastAPI
from app.api import accounts
from app.api import authentication, datasets, digitalcontracts, scn, dataFederation, datasetFamily, email, remoteDataConnector

server = FastAPI()

server.include_router(authentication.router)
server.include_router(accounts.router)
server.include_router(digitalcontracts.router)
server.include_router(datasetFamily.router)
server.include_router(datasets.router)
server.include_router(dataFederation.router)
server.include_router(scn.router)
server.include_router(remoteDataConnector.router)
server.include_router(email.router)
