from flask import Flask
from twilio_configure import send_message

from database import profile_data



app = Flask(__name__)

@app.route('/neuron-bot',methods=['POST'])
def home():
    print(profile_data)

    send_message("hii")
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)