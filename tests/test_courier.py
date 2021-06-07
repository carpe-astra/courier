from courier import __version__

from courier.models import Contact
from courier.notifications import send_text


def test_version():
    assert __version__ == "0.1.0"


def test_text():
    contact = {"name": "Taylor", "number": "530-748-9851", "carrier": "Verizon"}
    subject = "Testing..."
    message = "Just testing the Courier notification system!"

    send_text(contact, subject, message)
