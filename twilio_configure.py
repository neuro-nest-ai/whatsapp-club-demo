import logging

from twilio.rest import Client
from decouple import config

account_sid=config("TWILIO_ACCOUNT_SID")
auth_token=config("TWILIO_AUTH_TOKEN")

client=Client(account_sid,account_sid)
twilio_number=config("TWILIO_NUMBER")
to_number = config("TO_NUMBER")

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

def send_message(body_text):
    try:
        message=Client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
        )
        logger.info(f"Message sent to {to_number}:{message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}:{e}")