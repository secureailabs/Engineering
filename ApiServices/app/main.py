###################################################################################
# @author Prawal Gangwar
# @brief The main entrypoint of the API Services
# @License Private and Confidential. Internal Use Only.
# @copyright Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved.
###################################################################################

import fastapi.openapi.utils as utils
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, StrictStr

from app.api import (
    accounts,
    authentication,
    datasets,
    datasets_families,
    digital_contracts,
    internal_utils,
    remote_data_connector,
    secure_computation_nodes,
)

server = FastAPI(
    title="Secure AI Labs API Services",
    description="All the private and public APIs for the Secure AI Labs",
    version="0.1.0",
    docs_url=None,
)

# Add all the API services here exposed to the public
server.include_router(authentication.router)
server.include_router(accounts.router)
server.include_router(datasets.router)
server.include_router(digital_contracts.router)
server.include_router(secure_computation_nodes.router)
server.include_router(datasets_families.router)
server.include_router(remote_data_connector.router)
server.include_router(internal_utils.router)

# Override the default validation error handler as it throws away a lot of information
# about the schema of the request body.
class ValidataionError(BaseModel):
    error: StrictStr = Field(default="Invalid Schema")


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error = ValidataionError(error="Invalid Schema")
    return JSONResponse(status_code=422, content=jsonable_encoder(error))


utils.validation_error_response_definition = ValidataionError.schema()

# Run the uvicorn server
# uvicorn.run("app.main:server", host="127.0.0.1", port=8000, log_level="info")


@server.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    if server.openapi_url is None:
        raise RequestValidationError("openapi_url must be provided to serve Swagger UI")

    server.mount("/static", StaticFiles(directory="./app/static"), name="static")
    return get_swagger_ui_html(
        openapi_url=server.openapi_url,
        title=server.title + " - Swagger UI",
        oauth2_redirect_url=server.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
