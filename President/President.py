from twilio.rest import Client
import google.generativeai as genai 
import PIL.Image
import os                                    




# account_sid = os.getenv['TWILIO_ACCOUNT_SID']
# auth_token = os.getenv['TWILIO_AUTH_TOKEN']
# twilio_phone_number = os.getenv['TWILIO_NUMBER']

# board_members=[+919791339999,+919003535432,+919952203666,+919786000666,+919994496460,+919943030700,+918667259494,+919952705699,
            #    +919894408567,+919943434217,+919842279290,+919787770022,+919894727272,+919790087484,+919894847232,+917373200155,
            #    +919443374468,+919994200999,+919362022255,+919047077703,+919942872000,+919894054354,+919843298951,+919943515000,
            #    +919841345994,+919443081427,+919842288883,+919842213636,+919894646469]
# club_members=[+917373717788,+919994499988,+919366629909,+919095675000,+919894077567,+919894061764,+919047052848,+919360230187,
            #   +919345555663,+919894733996,+919444999400,+919894145962,+919843111300,+919443388633,+919842223788,+919843265775,
            #   +919842257423,+919600722590,+919865036199,+919842257106,+919366629909,+919894840490,+91984298812,+919894747660,
            #   +919600920774,+918056765999,+918508003335,+919443724266,+919488836000,+918754230343,+919486776061,+918220870701,
            #   +919003355555,+919600978460,+919894019019,+919443016545,+919843040051,+919842227273,+919994315167,+919043390434,
            #   +919865140077,+919442533480,+919487895554,+919443185595,+919597075043]
board_members=[+919942620943]
club_members=[+919360339999]

class President:
    def __init__(self):
        pass
    
    def generate_invitation(self,uploaded_image):
        prompt="extract the details and make invitation in english"
        image=PIL.Image.open(uploaded_image)
        vision_model = genai.GenerativeModel('gemini-pro-vision')
        response = vision_model.generate_content([prompt,image])
        text=response.text
        print(text)
        return text

    # def send_invitation(self,invitation_text, recipient_phone_number):
    #     client = Client(account_sid, auth_token)
    #     message = client.messages.create(body=invitation_text,
    #                                      from_=twilio_phone_number,to=recipient_phone_number)
    #     print(f"Invitation sent to {recipient_phone_number}! Message SID: {message.sid}")


    
    def send_messages_to_bord_members(self,text):
        for recipient_phone_number in board_members:
            self.send_invitation(text, recipient_phone_number)
            print("message sent")

    def send_messages_to_club_members(self,text):
        for recipient_phone_number in club_members:
            self.send_invitation(text, recipient_phone_number)
            print("message sent")
    

class President_send_message:
    def __init__(self):
        pass 

    def send_text_to_board_members(self,message):
        president=President()
        for recipient_phone_number in board_members:
            president.send_messages_to_bord_members(message,recipient_phone_number)

    def send_text_to_club_members(self,message):
        president=President()
        for recipient_phone_number in club_members:
            president.send_messages_to_club_members(message,recipient_phone_number)
            
            
# class Presidentconfig:
    # def __init__(self):
        # pass
    # 
    # def main(self,text):
        # president=President
# 



