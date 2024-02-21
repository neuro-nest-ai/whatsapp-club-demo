import logging
from twilio.rest import Client
#from decouple import config
import requests
import os

#Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Get Twilio credentials from environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
to_number = os.getenv("TO_NUMBER")

#Initialize Twilio client
client = Client(account_sid, auth_token)

def get_image(url):
    try:
        response = requests.get(url, auth=(account_sid, auth_token))
        return response
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

def send_message(body_text):
    try:
        #Send message using Twilio client
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
        )
        #Log message sent
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        #Log error if message sending fails
        logger.error(f"Error sending message to {to_number}: {e}")


