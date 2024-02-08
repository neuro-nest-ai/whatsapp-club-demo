import PIL
import google.generativeai as genai
#import mysql.connector
from twilio.rest import Client
from flask import Flask, request
#from Login_data.first_login import WhatsAppChatbot
from datetime import datetime
from database import profile_data,club,trust

class Dues:
    def __init__(self):
        pass

    def extract_payment_details(self,image_path):
        def dict_data(data_list):
            return {data_list[i].strip(','): data_list[i + 1].strip(',') for i in range(0, len(data_list), 2)}
        try:
            image = PIL.Image.open(image_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None
    
        wes = []
        wes2 = []
        vision_model = genai.GenerativeModel('gemini-pro-vision')

        # Updated prompt with 'UTR' instead of 'Account Number'
        prompt = """
        Extract the following payment details from the provided image:
        1. Amount (remove commas if present)
        2. Bank Number (4-digit integer) or Account Number
        3. UTR or UPI Transaction ID (12-digit)

        Ensure the response is in dictionary format with keys as follows:
        {
        "amount": <extracted_amount>,
       "bank_number_or_account": <extracted_bank_number_or_account>,
        "UTR_or_UPI_transaction_ID": <extracted_UTR_or_UPI_transaction_ID>
       }"""
        response = vision_model.generate_content([prompt, image])
        string_data = response.text
        for con in string_data.split():
            wes.append(con)
        data_list = wes[2:-2]
        for data in data_list:
            data = data.replace(":", "")
        wes2.append(data)
        new_list = [element.replace('"', '') for element in wes2]
        data_dict = dict_data(new_list)
        if 'amount' in data_dict and ('bank_number_or_account' in data_dict or 'account' in data_dict) and 'UTR_or_UPI_transaction_ID' in data_dict:
            return data_dict['amount'],data_dict['bank_number_or_account'],data_dict['UTR_or_UPI_transaction_ID']
        else:
            return str("something went wrong")

    def extract_whatsapp_number(self, sender_id):
        return request.form.get("From")

    def get_name_from_dict(self):
        phone_number=self.extract_whatsapp_number()
        for item in profile_data:
            if item.get('Mobile Phone') == phone_number:
                return item.get('Name')

    def insert_into_database(self,image_path,sender_id,Subscription="default"):
        Phone_number=self.extract_whatsapp_number(sender_id)
        Name=self.get_from_dict()
        Amount,Bank_number,UPI_traction_id=self.extract_payment_details(image_path)
        Date=datetime.now()
        if str(Bank_number).endswith('39'):
                Bank_number='39'
                if Amount<=15000:
                     Subscription=="Half yearly Subscription"
                else:
                    Subscription=="Yearly Subscription"
                print("Inserted successfully for phone_number ending with '39'")
                club_dict={}
                club_dict["Date"]=Date
                club_dict["Name"]=Name
                club_dict["Amount"]=Amount
                club_dict["Subscription"]=Subscription
                club_dict["Phone_number"]=Phone_number
                club_dict["Bank_number"]=Bank_number
                club_dict["UPI_traction_id"]=UPI_traction_id
                club.append(club_dict)
                self.send_whatsapp_message("The payment is done by {},{} and {} on {} to club_account and reply yes for confirmation".format
                           (Name,Amount,UPI_traction_id,Date))

        elif str(Bank_number).endswith('55'):
                Bank_number='55'
                Subscription="Your 80GT certificate will shortly come"
                print("Inserted successfully data into club_account")
                trust_dict={}
                trust_dict["Date"]=Date
                trust_dict["Name"]=Name
                trust_dict["Amount"]=Amount
                trust_dict["Subscription"]=Subscription
                trust_dict["Phone_number"]=Phone_number
                trust_dict["Bank_number"]=Bank_number
                trust_dict["UPI_traction_id"]=UPI_traction_id
                trust.append(trust_dict)
                self.send_whatsapp_message("The payment is done by {},{} and {} on {} to trust account and reply yes for confirmation".format
                                           (Name,Amount,UPI_traction_id,Date))
        else:
            print("Please upload screenshot")


    def send_whatsapp_message(self,message):
        try:
            # Initialize Twilio client
            account_sid = 'your_twilio_account_sid'
            auth_token = 'your_twilio_auth_token'
            twilio_whatsapp_number = 'whatsapp:+14155238886'
            recipient_whatsapp_number = 'whatsapp:+919488836000'
            client = Client(account_sid, auth_token)

            # Send WhatsApp message
            # Your Twilio WhatsApp number
            message = client.messages.create(
                body=message,
                from_=twilio_whatsapp_number,
                to=recipient_whatsapp_number  # Replace with actual recipient's phone number
            )
            print(f"WhatsApp message sent: {message.sid}")

        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")




#Screenshot Pipeline             
class Screenshot_pipeline:
    def __init__(self):
        pass
    def main(self,sender_id,image_path):
        dues_instance = Dues()
        dues_instance.get_name_from_database(sender_id,image_path)
               


