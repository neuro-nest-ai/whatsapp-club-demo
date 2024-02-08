from flask import Flask,request
from twilio_configure import send_message
from twilio.twiml.messaging_response import MessagingResponse

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
    

@app.route('/neuron-bot',methods=['POST'])
def home():
    incoming_request = request.form.to_dict(flat=False)
    message_sent_by_user = incoming_request['Body'][0]
    # Generate the answer using GPT-3
    answer = generate_answer(message_sent_by_user)
    
    if(userFirstLogin(incoming_request['From'][0],incoming_request['ProfileName'][0])):
        print("hii",users)
        return "ok"
    
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)