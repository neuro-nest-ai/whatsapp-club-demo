import logging
from twilio.rest import Client
#from decouple import config
import requests
import os

#Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Get Twilio credentials from environment variables
account_sid = "AC5c770f9ab12adfc23d89befc8bebad6c"
print(account_sid)
auth_token = '1a13bc4e337930fc2a4417327cb7d493'
print(auth_token)
twilio_number = "+14155238886"
print(twilio_number)
to_number = "+918861842522"
print(to_number)

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


