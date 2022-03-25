#!/usr/bin/env python3
__author__ = "Prawal Gangwar"
__copyright__ = "Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved."
__license__ = "Private and Confidential. Internal Use Only."
__date__ = "25 March 2022"
__file__ = "main.py"

from fastapi import FastAPI
from pydantic import BaseModel, StrictStr
import sendEmail
from sendEmail import SenderCredentials

emailPlugin = FastAPI()


class ForgotPassswordRequest(BaseModel):
    Recepient: StrictStr
    Sender: SenderCredentials
    Secret: StrictStr


@emailPlugin.post("/Email/forgotPassword")
async def forgotPassword(request: ForgotPassswordRequest):
    subject = "Secure AI Labs - Reset Password"
    body = sendEmail.getForgetPasswordContent(request.Secret)
    sendEmail.sendEmail(
        sender=SenderCredentials(email=request.Sender.email, password=request.Sender.password),
        recepient=request.Recepient,
        subject=subject,
        body=body,
    )
    return "Success"


class VerifyEmailRequest(BaseModel):
    Recepient: StrictStr
    Sender: SenderCredentials
    Secret: StrictStr


@emailPlugin.post("/Email/verifyEmail")
async def verifyEmail(request: VerifyEmailRequest):
    subject = "Welcome to Secure AI Labs. Let's verify your email!"
    body = sendEmail.getVerifyEmailContent(request.Secret)
    sendEmail.sendEmail(
        sender=SenderCredentials(email=request.Sender.email, password=request.Sender.password),
        recepient=request.Recepient,
        subject=subject,
        body=body,
    )
    return "Success"


class AlertRequest(BaseModel):
    Recepient: StrictStr
    Sender: SenderCredentials
    Alert: StrictStr


@emailPlugin.post("/Email/alert")
async def alert(request: AlertRequest):
    subject = "Important Alert:" + request.Alert
    body = sendEmail.getAlertContent(request.Alert)
    sendEmail.sendEmail(
        sender=SenderCredentials(email=request.Sender.email, password=request.Sender.password),
        recepient=request.Recepient,
        subject=subject,
        body=body,
    )
    return "Success"
