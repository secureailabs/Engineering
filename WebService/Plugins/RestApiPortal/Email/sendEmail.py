import smtplib
from pydantic import BaseModel, StrictStr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, status


class SenderCredentials(BaseModel):
    email: StrictStr
    password: StrictStr


def getForgetPasswordContent(secret: str):
    htmlText = """
        <html>
            <head></head>
            <body>
                Hello, <br><br> <br>Visit to reset your password: <a href = "http://www.secureailabs.com">http://www.secureailabs.com/"""+secret+"""</a>
            </body>
        </html>
    """
    return htmlText


def getVerifyEmailContent(secret: str):
    htmlText = """
        <html>
            <head></head>
            <body>
                Hello, <br><br> <br>Visit to verify your email: <a href = "http://www.secureailabs.com">http://www.secureailabs.com/"""+secret+"""</a>
            </body>
        </html>
    """
    return htmlText


def getAlertContent(alert: str):
    htmlText = """
        <html>
            <head></head>
            <body>
                Hello, <br><br> Unusual activity detected on your account: <a href = "http://www.secureailabs.com">http://www.secureailabs.com/"""+alert+"""</a>
            </body>
        </html>
    """
    return htmlText


def sendEmail(sender: SenderCredentials, recepient: str, subject: str, body: str):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = 'Secure AI Labs <' + sender.email + '>'
    message['To'] = recepient
    part1 = MIMEText(body, 'html')
    message.attach(part1)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender.email, sender.password)
        server.sendmail(sender.email, [recepient], message.as_string())
        server.close()
    except smtplib.SMTPResponseException as exception:
        raise HTTPException(status_code=exception.smtp_code, detail=str(exception.smtp_error))
    except smtplib.SMTPRecipientsRefused as exception:
        raise HTTPException(status_code=450, detail="Failed sending email to: " + str(exception))
    except smtplib.SMTPServerDisconnected:
        raise HTTPException(status_code=554, detail="Server unexpectedly disconnected or an attempt is made to use \
            the SMTP instance before connecting it to a server")
    except smtplib.SMTPNotSupportedError:
        raise HTTPException(status_code=status.HTTP_510_NOT_EXTENDED, detail="The command or option is not \
            supported by the SMTP server")
    except smtplib.SMTPException:
        raise HTTPException(status_code=status.HTTP_510_NOT_EXTENDED, detail="Unknown SMTP error. Should not happen")
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Send Email \
            Error: " + str(exception))
