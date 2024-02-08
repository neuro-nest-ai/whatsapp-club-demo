import logging
from twilio.rest import Client
from decouple import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Twilio credentials from environment variables
account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
twilio_number = config("TWILIO_NUMBER")
to_number = config("TO_NUMBER")

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_message(body_text):
    try:
        # Send message using Twilio client
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
        )
        # Log message sent
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        # Log error if message sending fails
        logger.error(f"Error sending message to {to_number}: {e}")



