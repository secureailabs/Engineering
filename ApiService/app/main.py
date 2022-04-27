from fastapi import FastAPI
from ApiService.app.api import accounts
from app.api import authentication, datasets, digitalcontracts, scn

server = FastAPI()

server.include_router(accounts.router)
server.include_router(authentication.router)
server.include_router(datasets.router)
server.include_router(digitalcontracts.router)
server.include_router(scn.router)
