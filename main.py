import re
import os
from dateutil import parser
import google.generativeai as palm
from utilis import is_image
from Screen_shot import PaymentPipeline
from President.President import President_send_message, President
from Treasurer.Reply import ReplyConfig
from Pdf_Question.pdf_question import pdf_pipeline
import datefinder
from Rotary_club_Question import pdf_questions
from report_generation import PdfPipelineConfig





from Pdf_generation.trust_certificate import scannedPdfConverter
#from test import generate_invoice
from pdf_pipe_line import PdfPipelineConfig
save_path = r"output.pdf"

save_path = r"output.pdf"
file_path_profile=r"Data\Members profile sample.pdf"
scannedPdfConverter(file_path_profile,save_path)     





# Make sure to set your Google API key properly
GOOGLE_API_KEY = "AIzaSyB2pkELdV1dA8ylaKlqV4wXN8HPK26sGp0"
palm.configure(api_key=GOOGLE_API_KEY)

def extract_datetime(text):
    datetime_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}-\d{1,2}-\d{4}\b')
    matches = datetime_pattern.findall(text)
    datetime_objects = [parser.parse(match, fuzzy=True) for match in matches]
    return datetime_objects


   
def image_details(question):
    screen_shot = PaymentPipeline()
    details=screen_shot.main_path(question)
    if details!="Please upload screen_shot":
        print("Payment done")
        return str("Payment successfully done")
    else:
        print("invitation")
        invitation = President()
        text=invitation.generate_invitation(question)
        #invitation.send_messages_to_board_members(image, question)
        return text # Corrected argument
def generate_answer(question):
        save_path_base = "output"
        key_words_Donation = ["need to donation", "need to donate", "need to contribution","need to contribute"]
        key_words_Dues = ["pay dues", "need registration","need to subscription"]
        key_words_generation = ['report', 'generation', 'report generation']
        President_key_words_board = ["board_members", 'board members']
        President_key_words_club_members = ["club_members", 'club members']
        pattern = re.compile(r'^yes (\d{12}) trust$', re.IGNORECASE)
        # Added re.IGNORECASE
        question = question.lower()
        response = palm.chat(messages=question, temperature=0.8, context="you are assistance bot give 5 lines")
        if any(keyword in response.messages[0]['content'].lower() for keyword in key_words_generation):
            text1 = input("Please enter the end date (format: YYYY-MM-DD):")
            start_date_input1 = input(text1)
            start_date1= parser.parse(start_date_input1, fuzzy=True)
            text2=input("Please enter the end date (format: YYYY-MM-DD):")
            start_date_input2=input(text2)
            start_date2=parser.parser(start_date_input2,fuzzy=True)
            config=PdfPipelineConfig()
            pdf_path=config.main(start_date1,start_date_input2,save_path_base)
            return pdf_path
            
            
            
            
            return text
        elif re.search(pattern, response.messages[0]['content']):  # Removed re.IGNORECASE
            data_config = ReplyConfig()
            _, trust = data_config.main(response.messages[0]['content'])
            if trust:
                invoice=PdfPipelineConfig()
                pdf=invoice.main(response.messages[0]['content'],save_path)
                return pdf
            else:
                invoice=PdfPipelineConfig()
                pdf=invoice.main(response.messages[0]['content'],save_path)
                return pdf
            
        elif any(keyword in response.messages[0]["content"].lower() for keyword in President_key_words_board):
            send_message = President_send_message()
            send_message.send_text_to_board_members(response.messages[0]["content"])
        elif any(keyword in response.messages[0]["content"].lower() for keyword in President_key_words_club_members):
            send_message = President_send_message()
            send_message.send_text_to_board_members(response.messages[0]["content"])
        elif any(keyword in response.messages[0]['content'].lower() for keyword in key_words_Donation):
            text = """Trust Account - Rotary club of Trust
                    Account number - 9446903739
                    IFSC code - KKBK0008664
                    Kotak Mahindra bank Trichy road branch Coimbatore
                    Please pay for above accounts and upload screen shot with UTR number\with UPI_transaction"""
            return text
        elif any(keyword in response.messages[0]['content'].lower() for keyword in key_words_Dues):
            text = """Club Account - Rotary club of Coimbatore North
                   Account number - 6048270955
                   IFSC code - KKBK0008664
                   Kotak Mahindra bank Trichy road branch Coimbatore
                   Please pay for above accounts and upload screen shot with UTR number\with UPI_transaction"""
            return text
        elif datefinder.find_dates(response.messages[0]['content']):
            date = extract_datetime(response.messages[0]['content'])
            if date:
                return "report generation pdf"
        
            else:
                data=pdf_questions(response.messages[0]['content'])
                if "I am not answer"  not in data:
                    return data
                else:
                    return response.messages[1]['content']