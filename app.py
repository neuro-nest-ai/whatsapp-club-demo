from flask import Flask,request
from twilio_configure import send_message

from database import profile_data,users



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
    
    if(userFirstLogin(incoming_request['From'][0],incoming_request['ProfileName'][0])):
        print("hii",users)
        return "ok"
    
    send_message("hii")
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)