"""Main notifications API"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Union

from courier.config import settings, EmailServerSettings, CARRIERS_FILEPATH
from courier.models import Contact, CarrierList

with open(CARRIERS_FILEPATH) as f:
    CARRIER_LIST = CarrierList(carriers=json.load(f))


class EmailServer(object):
    def __init__(self, settings: EmailServerSettings):
        self.settings = settings
        self.server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        self.server.starttls()
        self.server.login(settings.email, settings.password)

    def __enter__(self):
        return self.server

    def __exit__(self, type, value, traceback):
        self.server.quit()

    def sendmail(self, recipients: List[str], subject: str = None, body: str = None):
        message = MIMEMultipart()

        message["Subject"] = subject
        message["From"] = settings.email
        message["To"] = ", ".join(recipients)
        message.attach(MIMEText(body, "plain"))

        self.server.sendmail(self.settings.email, recipients, message.as_string())


EMAIL_SERVER = EmailServer(settings)


def send_email(recipients: Union[List[str], str], subject: str, body: str):
    if isinstance(recipients, str):
        recipients = [recipients]

    EMAIL_SERVER.sendmail(recipients, subject, body)


def send_text(contacts: Union[List[dict], dict], subject: str, message: str):
    if isinstance(contacts, dict):
        contacts = [contacts]

    recipients = []
    for contact_dict in contacts:
        contact = Contact(**contact_dict)
        carrier = next(
            (
                carrier
                for carrier in CARRIER_LIST.carriers
                if carrier.name == contact.carrier
            ),
            None,
        )
        if carrier is None:
            raise ValueError(f"Unknown carrier: {contact.carrier}")

        number = contact.number.replace("-", "")
        recipient = number + carrier.extension
        recipients.append(recipient)

    send_email(recipients, subject, message)
