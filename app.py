from flask import Flask,request
from twilio_configure import send_message
from twilio.twiml.messaging_response import MessagingResponse
import requests
from database import profile_data,users
from main import generate_answer



app = Flask(__name__)



def userFirstLogin(mobileNumber,profileName):
    global users
    for i in users:
        if(i['mobile_number'] == mobileNumber):
            return False 
    users.append({'name':'praveen','mobile_number':'9486706677'})
    # print(users)
    return True
    

@app.route('/welcome',methods=['POST'])
def home():
    #incoming_que = request.form['message']  # Assuming 'message' is the name of the input field containing user messages

    #incoming_request = request.form.to_dict(flat=False)
    incoming_que = request.values.get('Body', '').lower()
    media_url = request.values.get('MediaUrl', '')
    print("Question: ", incoming_que)
    print("Question",media_url)



    if media_url:

        response = requests.get(media_url)
        if response.status_code == 200:
            image_data = response.content
            answer = generate_answer(image_data)
        else:
            answer = "Error: Unable to fetch media content"
       
    else:
        answer=generate_answer(incoming_que)

    #message_sent_by_user = incoming_request['Body'][0]
    # Generate the answer using GPT-3
    #answer = generate_answer(incoming_que)
    
    #if(userFirstLogin(incoming_request['From'][0],incoming_request['ProfileName'][0])):
    #print("hii",users)
        #return "ok"
    
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)