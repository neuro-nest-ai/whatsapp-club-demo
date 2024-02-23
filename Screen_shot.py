from PIL import Image
import pandas as pd
from data_dict import profile_data, trust, club
import google.generativeai as genai
from pathlib import Path
import datetime

class Dues:
    def __init__(self):
        pass
    
    def extract_payment_details(self, image_path):
        try:
             def dict_data(data_list):
                 return {data_list[i].strip(','): data_list[i + 1].strip(',') for i in range(0, len(data_list), 2)}
            
        except Exception as e:
            return "Please upload a valid screenshot."

        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

        try:
            wes = []
            wes2 = []
            vision_model = genai.GenerativeModel('gemini-pro-vision')
            prompt = """
            Extract the following payment details from the provided image:
            1. Amount (remove commas if present)
            2. Bank Number (4-digit integer) or Account Number
            3. UTR or UPI Transaction ID (12-digit)
            Ensure the response is in dictionary format with keys as follows:
            {
            "amount": <extracted_amount>,
            "bank_number_or_account": <extracted_bank_number_or_account>,
            "UTR_or_UPI_transaction_ID": <extracted_UTR_or_UPI_transaction_ID>}"""
            response = vision_model.generate_content([prompt, image])
            string_data = response.text
            print(string_data)
            for con in string_data.split():
                print(con)
                wes.append(con)
            print(wes)
            data_list = wes[2:-2]
            print(data_list)
            for data in data_list:
                data = data.replace(":", "")
                wes2.append(data)
            print(wes2)
            new_list = [element.replace('"', '') for element in wes2]
            print(len(new_list))
            if len(new_list)==6 and "not" not in new_list:
                data_dict = dict_data(new_list)
                if data_dict!="Please upload a valid screenshot.":
                    if 'amount' in data_dict and ('bank_number_or_account' in data_dict or 'account' in data_dict) and 'UTR_or_UPI_transaction_ID' in data_dict:
                        print(data_dict['amount'], data_dict['bank_number_or_account'], data_dict['UTR_or_UPI_transaction_ID'])
                        return int(data_dict['amount']), int(data_dict['bank_number_or_account']), str(data_dict['UTR_or_UPI_transaction_ID'])
            else:   
                return "Something went wrong"
        except Exception as e:
            return "Something went wrong"
    
    def get_name_from_dict(self, phone_number='91 7373200155'):
        for item in profile_data:
            if item.get('Mobile Phone') == phone_number:
                return item.get('Name')
        return None

    def insert_into_database(self, image_path, phone_number='91 7373200155'):
        Name = self.get_name_from_dict(phone_number)
        payment_details = self.extract_payment_details(image_path)
        if payment_details!="Something went wrong":
            Amount, Bank_number, UPI_transaction_id = payment_details
            Date = datetime.date.today()
            
            if str(Bank_number).endswith('55'):
                df = pd.read_csv('Data/club.csv')
                Invoice_number = df['Invoice_No'].max() or 0
                Invoice_number += 1
                Invoice_number = str(Invoice_number).zfill(2)
                Bank_number = '55'
                Subscription = "Half yearly Subscription" if float(Amount) <= 15000 else "Yearly Subscription"
                print("Inserted successfully for phone_number ending with '39'")
                club_dict = {
                    "Date": Date,
                    "Name": Name,
                    "Amount": Amount,
                    "Subscription": Subscription,
                    "Phone_number": phone_number,
                    "Bank_number": Bank_number,
                    "UPI_transaction_id": UPI_transaction_id,
                    "Invoice_No": Invoice_number
                }
                club.append(club_dict)
                return club_dict, str("club")
                
            else:
                str(Bank_number).endswith('39')
                df = pd.read_csv('Data\Trust_details.csv')
                Invoice_number = df['Receipt_No'].max() or 0
                Invoice_number += 1
                Invoice_number = str(Invoice_number).zfill(2)
                Bank_number = '39'
                Subscription = "Donation"
                print("Inserted successfully data into trust_account")
                trust_dict = {
                    "Date": Date,
                    "Name": Name,
                    "Amount": Amount,
                    "Project": Subscription,
                    "Mobile Phone": phone_number,
                    "Bank_number": Bank_number,
                    "UPI_transaction_id": UPI_transaction_id,
                    "Receipt_No": Invoice_number
                }
                return trust_dict, str("trust")
        else:
            return str("Payment details extraction failed")

class ScreenshotPipeline:
    def __init__(self):
        pass
    
    def main(self, image_path):
        dues_instance = Dues()
        data= dues_instance.insert_into_database(image_path)
        return data

class PaymentPipeline:
    def __init__(self):
        pass
    
    def main_path(self, image_path):
        pipeline = ScreenshotPipeline()
        payment= pipeline.main(image_path)
        if type(payment)==tuple:
            (data, x)=payment
            if x == "club":
                df = pd.read_csv('Data/club.csv')
                new_row_df = pd.DataFrame([data])
                df = pd.concat([df, new_row_df], ignore_index=True)
                df.to_csv('Data/club.csv', index=False)
                return str("done")
            else:
                df = pd.read_csv('Data\Trust_details.csv')
                new_row_df = pd.DataFrame([data])
                df = pd.concat([df, new_row_df], ignore_index=True)
                df.to_csv('Data\Trust_details.csv', index=False)
                return str("done")
        else:
            return str("Please upload screen_shot")


#Define the path to your image
# image_path = Path("Image_data") / "WhatsApp Image 2024-01-19 at 12.18.18_561c454a.jpg"
# payment = PaymentPipeline()
# payment.main_path(image_path)