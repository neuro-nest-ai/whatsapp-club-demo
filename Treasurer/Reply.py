import re
from twilio.rest import Client
import os

#TWILIO_ACCOUNT_SID = os.getenv['TWILIO_ACCOUNT_SID']
#TWILIO_AUTH_TOKEN= os.getenv['TWILIO_AUTH_TOKEN']
#TWILIO_PHONE_NUMBER = os.getenv['TWILIO_NUMBER']


# Your regex pattern for extracting amount, phone numbers, and trust
import re

message_pattern = re.compile(r'^verified (\d{12}) trust account$')

                             

class SenderConfig:
    def __init__(self):
        pass

    def extract_data(self, message):
        message=message.split()
        UPI_traction_id=message[1]
        text1=message[2]
        account=message[3]
        trust=text1+" "+account
        
        return str(UPI_traction_id),trust

    #def send_twilio_sms(self, to, body):
    #client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    #message = client.messages.create(
    #to=to,
    #from_=TWILIO_PHONE_NUMBER,
    #body=body)
        #return message


class ReplyConfig:
    def __init__(self):
        pass

    def main(self, received_message):
        sender = SenderConfig()
        UPI_traction_id,trust= sender.extract_data(received_message)
        return str(UPI_traction_id),trust






