# -------------------------------------------------------------------------------
# Engineering
# main.py
# -------------------------------------------------------------------------------
"""The main entrypoint of the API Services"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import logging
import threading

import fastapi.openapi.utils as utils
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_responses import custom_openapi
from pydantic import BaseModel, Field, StrictStr

from app.api import (
    accounts,
    authentication,
    data_federations,
    data_federations_provisions,
    dataset_versions,
    datasets,
    internal_utils,
    secure_computation_nodes,
)
from app.log import _AsyncLogger, log_message

server = FastAPI(
    title="SAIL",
    description="All the private and public APIs for the Secure AI Labs",
    version="0.1.0",
    docs_url=None,
)
server.openapi = custom_openapi(server)


class Audit_log_task(threading.Thread):
    """
    Auxillary class for audit log server in isolated thread
    """

    def run(self):
        """
        Start async logger server
        """
        _AsyncLogger.start_log_poller(_AsyncLogger.ipc, _AsyncLogger.port)


# Add all the API services here exposed to the public
server.include_router(authentication.router)
server.include_router(accounts.router)
server.include_router(data_federations.router)
server.include_router(data_federations_provisions.router)
server.include_router(datasets.router)
server.include_router(dataset_versions.router)
server.include_router(secure_computation_nodes.router)
server.include_router(internal_utils.router)


# Override the default validation error handler as it throws away a lot of information
# about the schema of the request body.
class ValidationError(BaseModel):
    error: StrictStr = Field(default="Invalid Schema")


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error = ValidationError(error="Invalid Schema")
    return JSONResponse(status_code=422, content=jsonable_encoder(error))


@server.exception_handler(Exception)
async def server_error_exception_handler(request: Request, exc: Exception):
    """
    Handle all unknown exceptions

    :param request: The http request object
    :type request: Request
    :param exc: The exception object
    :type exc: Exception
    """
    message = f"Unkown Exception: {str(exc)} in request: {request.method} {request.url}"
    # Log the error to the uvicorn logger
    logger = logging.getLogger("uvicorn.error")
    logger.error(message)
    # Add the exception to the audit log as well
    await log_message(message)


utils.validation_error_response_definition = ValidationError.schema()


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


@server.on_event("startup")
async def start_audit_logger():
    """
    Start async audit logger server at start up as a background task
    """
    t = Audit_log_task()
    t.start()
