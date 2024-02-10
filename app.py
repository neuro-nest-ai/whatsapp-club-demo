from flask import Flask,request
import logging
from twilio_configure import send_message,get_image
from twilio.twiml.messaging_response import MessagingResponse
import requests
from database import profile_data,users
from main import generate_answer,image_details
import io



app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def userFirstLogin(mobileNumber,profileName):
    global users
    for i in users:
        if(i['mobile_number'] == mobileNumber):
            return False 
    users.append({'name':'praveen','mobile_number':'9486706677'})
    # print(users)
    return True

DOWNLOAD_DIRECTORY = 'Treasurer'




    

@app.route('/welcome',methods=['POST'])
def home():
    #incoming_que = request.form['message']  # Assuming 'message' is the name of the input field containing user messages

    #incoming_request = request.form.to_dict(flat=False)
    incoming_que = request.values.get('Body', '').lower()
    media_msg = request.form.get('NumMedia') 
    print("Question: ", request.form.to_dict(flat=False))
    print("Question",media_msg)
    
    media = request.form.to_dict(flat=False)
    media_url = media['MediaUrl0']
    media_to = media['From'][0]
    media_type = media['MediaContentType0']
    try:
        image = get_image(media_url[0])
        with open(f'{DOWNLOAD_DIRECTORY}/{media_to}/sample.jpeg', 'wb') as f:
           f.write(image.content)
    except Exception as e:
        logger.error(f"Error while creating the image : {e}")
     
    return "ok"   
    



    
    
    
    
                 #answer = generate_answer(pic_url)
            #else:
                 
    #message_sent_by_user = incoming_request['Body'][0]
    # Generate the answer using GPT-3
    #answer = generate_answer(incoming_que)
    
    #if(userFirstLogin(incoming_request['From'][0],incoming_request['ProfileName'][0])):
    #print("hii",users)
        #return "ok"
   
    
    # bot_resp = MessagingResponse()
    # msg = bot_resp.message()
    # if media_msg:
    #      pic_url = request.form.get('MediaUrl0')
    #      if pic_url:
    #          answer=pic_url
    #          print("BOT Answer: ", answer.content)
    #         #  msg = bot_resp.message("Thanks for the image").media(answer)
    #         #  msg.body(msg)
    #      else:
    #         answer=generate_answer(incoming_que)
    #         print("BOT Answer: ", answer)
            
    #         msg.body(answer)
    # return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)