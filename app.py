from flask import Flask,request
import logging
from twilio_configure import send_message,get_image
from twilio.twiml.messaging_response import MessagingResponse
import requests
from main import generate_answer,image_details
import io
import uuid




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



def get_path(media_url,DOWNLOAD_DIRECTORY):
    image = get_image(media_url[0])
    unique_filename = str(uuid.uuid4()) + ".jpeg"
    with open(f'{DOWNLOAD_DIRECTORY}/{unique_filename}','wb') as f:
        f.write(image.content)
        image_path = f'{DOWNLOAD_DIRECTORY}/{unique_filename}'
    return image_path

DOWNLOAD_DIRECTORY = 'Image_data'  
    
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print(request.json)
    if request.method == 'POST':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        
    
        if mode == 'subscribe' and token == "123456":
            return challenge, 200
        else:
            return 'Verification failed', 403
    elif request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
    
        if mode == 'subscribe' and token == "123456":
            return challenge, 200
        else:
            return 'Verification failed', 403
         
     
    
    
    
    
    
    



@app.route('/welcome',methods=['POST'])
def home():
    #incoming_que = request.form['message']  # Assuming 'message' is the name of the input field containing user messages

    #incoming_request = request.form.to_dict(flat=False)
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", request.form.to_dict(flat=False))
    
    
    if request.values['NumMedia'] != '0':
        media = request.form.to_dict(flat=False)
        media_url = media['MediaUrl0']
    #media_to = media['From'][0]
    
    #media_type = media['MediaContentType0']
    #message_sent_by_user = incoming_request['Body'][0]
    # Generate the answer using GPT-3
    #answer = generate_answer(incoming_que)
    
    #if(userFirstLogin(incoming_request['From'][0],incoming_request['ProfileName'][0])):
    #print("hii",users)
        #return "ok"
   
    
        if media_url:
            try:
                image_path=get_path(media_url,DOWNLOAD_DIRECTORY)
                print("Image saved at:", image_path)
                answer=image_details(image_path)
            except Exception as e:
                logger.error(f"Error while creating the image : {e}")
    else:
        answer=generate_answer(incoming_que)
        print("BOT Answer: ", answer)
        
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000) 