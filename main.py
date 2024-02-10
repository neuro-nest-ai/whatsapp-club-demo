import re
import os
from dateutil import parser
import google.generativeai as palm
from utilis import is_image
from financial.Screen_shot import Screenshot_pipeline
from President.President import President_send_message, President
from Treasurer.Reply import ReplyConfig
from Pdf_Question.pdf_question import pdf_pipeline
import datefinder

# Make sure to set your Google API key properly
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
palm.configure(api_key=GOOGLE_API_KEY)

def extract_datetime(text):
    datetime_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}-\d{1,2}-\d{4}\b')
    matches = datetime_pattern.findall(text)
    datetime_objects = [parser.parse(match, fuzzy=True) for match in matches]
    return datetime_objects


   
def image_details(question,sender_id=None):
    screen_shot = Screenshot_pipeline()
    payment = screen_shot.main(question)
    print("sucessfully inserted")
    if payment:
        return "Payment successfully done"
    else:
        return "upload proper screen shot"
    #else:
        #invitation = President()
        #invitation.send_messages_to_board_members(image, question)
        #return str("iam king")  # Corrected argument
def generate_answer(question):
        key_words_Donation = ["donation", "donate", "contribution","contribute"]
        key_words_Dues = ["dues", "registration"]
        key_words_generation = ['report', 'generation', 'report generation']
        President_key_words_board = ["board_members", 'board members']
        President_key_words_club_members = ["club_members", 'club members']
        pattern = re.compile(r'^yes (\d{12}) trust$', re.IGNORECASE)  # Added re.IGNORECASE
        question = question.lower()
        response = palm.chat(messages=question, temperature=0.9, context="you are assistance bot give 5 lines")
        if any(keyword in response.messages[0]['content'].lower() for keyword in key_words_generation):
            text = "Please tell the Date in for YY/MM/DD of report generation"
            return text
        elif re.search(pattern, response.messages[0]['content']):  # Removed re.IGNORECASE
            data_config = ReplyConfig()
            _, trust = data_config.main(response.messages[0]['content'])
            if trust:
                return "we will issue 80GT certificate"
            else:
                return "we will issue invoice pdf"
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
                return response.messages[1]['content']
