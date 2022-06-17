# -------------------------------------------------------------------------------
# Engineering
# emails.py
# -------------------------------------------------------------------------------
"""APIs for Email Service"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, HTTPException, status
from models.emails import EmailRequest

router = APIRouter()

# TODO: Prawal Put them in IV or env
SAIL_EMAIL = "no-reply@secureailabs.com"
SAIL_PASSWORD = "something"

########################################################################################################################
# Since this is supposed to be a private API no public facing endpoints are needed
async def send_email(request: EmailRequest):
    message = MIMEMultipart()
    message["Subject"] = request.subject
    message["From"] = "Secure AI Labs <" + SAIL_EMAIL + ">"
    message["To"] = request.to
    part = MIMEText(request.body, "html")
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(SAIL_EMAIL, SAIL_PASSWORD)
        server.sendmail(SAIL_EMAIL, [request.to], message.as_string())
        server.close()
    except smtplib.SMTPResponseException as exception:
        raise HTTPException(status_code=exception.smtp_code, detail=str(exception.smtp_error))
    except smtplib.SMTPRecipientsRefused as exception:
        raise HTTPException(status_code=450, detail="Failed sending email to: " + str(exception))
    except smtplib.SMTPServerDisconnected:
        raise HTTPException(
            status_code=554,
            detail="Server unexpectedly disconnected or an attempt is made to use the SMTP instance before connecting it to a server",
        )
    except smtplib.SMTPNotSupportedError:
        raise HTTPException(
            status_code=510,
            detail="The command or option is not supported by the SMTP server",
        )
    except smtplib.SMTPException:
        raise HTTPException(status_code=510, detail="Unknown SMTP error. Should not happen")
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Send Email Error: " + str(exception),
        )
