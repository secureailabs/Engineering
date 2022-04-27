#!/usr/bin/env python3
__author__ = "Prawal Gangwar"
__copyright__ = "Copyright (C) 2022 Secure AI Labs, Inc. All Rights Reserved."
__license__ = "Private and Confidential. Internal Use Only."
__date__ = "25 March 2022"
__file__ = "main.py"

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, StrictStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

emailPlugin = FastAPI()


class SenderCredentials(BaseModel):
    email: StrictStr
    password: StrictStr


def getForgetPasswordContent(secret: str):
    htmlText = (
        """
        <html>
            <head></head>
            <body>
                Hello, <br><br> <br>Visit to reset your password:
                    <a href = "http://www.secureailabs.com">http://www.secureailabs.com/""" + secret + """</a>
            </body>
        </html>
    """
    )
    return htmlText


def getVerifyEmailContent(secret: str):
    htmlText = (
        """
        <html>
            <head></head>
            <body>
                Hello, <br><br> <br>Visit to verify your email: <a href = "http://www.secureailabs.com">http://www.secureailabs.com/""" + secret + """</a>
            </body>
        </html>
    """
    )
    return htmlText


def getAlertContent(alert: str):
    htmlText = (
        """
        <html>
            <head></head>
            <body>
                Hello, <br><br> Unusual activity detected on your account: <a href = "http://www.secureailabs.com">http://www.secureailabs.com/""" + alert + """</a>
            </body>
        </html>
    """
    )
    return htmlText


def sendEmail(sender: SenderCredentials, recepient: str, subject: str, body: str):
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = "Secure AI Labs <" + sender.email + ">"
    message["To"] = recepient
    part1 = MIMEText(body, "html")
    message.attach(part1)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(sender.email, sender.password)
        server.sendmail(sender.email, [recepient], message.as_string())
        server.close()
    except smtplib.SMTPResponseException as exception:
        raise HTTPException(status_code=exception.smtp_code, detail=str(exception.smtp_error))
    except smtplib.SMTPRecipientsRefused as exception:
        raise HTTPException(status_code=450, detail="Failed sending email to: " + str(exception))
    except smtplib.SMTPServerDisconnected:
        raise HTTPException(
            status_code=554,
            detail="Server unexpectedly disconnected or an attempt is made to use \
            the SMTP instance before connecting it to a server",
        )
    except smtplib.SMTPNotSupportedError:
        raise HTTPException(
            status_code=510,
            detail="The command or option is not \
            supported by the SMTP server",
        )
    except smtplib.SMTPException:
        raise HTTPException(status_code=510, detail="Unknown SMTP error. Should not happen")
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Send Email \
            Error: " + str(exception),
        )


class ForgotPassswordRequest(BaseModel):
    Recepient: StrictStr
    Sender: SenderCredentials
    Secret: StrictStr


@emailPlugin.post("/Email/forgotPassword")
async def forgotPassword(request: ForgotPassswordRequest):
    try:
        subject = "Secure AI Labs - Reset Password"
        body = sendEmail.getForgetPasswordContent(request.Secret)
        sendEmail.sendEmail(
            sender=SenderCredentials(email=request.Sender.email, password=request.Sender.password),
            recepient=request.Recepient,
            subject=subject,
            body=body,
        )
        return "Success"
    except HTTPException as exception:
        print("exception: ", exception.detail)
        raise HTTPException(status_code=exception.status_code, detail=exception.detail)


class VerifyEmailRequest(BaseModel):
    Recepient: StrictStr
    Sender: SenderCredentials
    Secret: StrictStr


@emailPlugin.post("/Email/verifyEmail")
async def verifyEmail(request: VerifyEmailRequest):
    try:
        subject = "Welcome to Secure AI Labs. Let's verify your email!"
        body = sendEmail.getVerifyEmailContent(request.Secret)
        sendEmail.sendEmail(
            sender=SenderCredentials(email=request.Sender.email, password=request.Sender.password),
            recepient=request.Recepient,
            subject=subject,
            body=body,
        )
        return "Success"
    except HTTPException as exception:
        print("exception: ", exception.detail)
        raise HTTPException(status_code=exception.status_code, detail=exception.detail)


class AlertRequest(BaseModel):
    Recepient: StrictStr
    Sender: SenderCredentials
    Alert: StrictStr


@emailPlugin.post("/Email/alert")
async def alert(request: AlertRequest):
    try:
        subject = "Important Alert:" + request.Alert
        body = sendEmail.getAlertContent(request.Alert)
        sendEmail.sendEmail(
            sender=SenderCredentials(email=request.Sender.email, password=request.Sender.password),
            recepient=request.Recepient,
            subject=subject,
            body=body,
        )
        return "Success"
    except HTTPException as exception:
        print("exception: ", exception.detail)
        raise HTTPException(status_code=exception.status_code, detail=exception.detail)
