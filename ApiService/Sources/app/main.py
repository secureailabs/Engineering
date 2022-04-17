from fastapi import FastAPI
from app.api import authentication, datasets, users, digitalcontracts, organization, scn

app = FastAPI()


app.include_router(organization.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(datasets.router)
app.include_router(digitalcontracts.router)
app.include_router(scn.router)
