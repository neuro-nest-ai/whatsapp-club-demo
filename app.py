from flask import Flask,request,jsonify
import logging
import requests
from main import generate_answer,image_details
import io
import json
import uuid
import os
from dotenv import load_dotenv




app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()



def userFirstLogin(mobileNumber,profileName):
    global users
    for i in users:
        if(i['mobile_number'] == mobileNumber):
            return False 
    users.append({'name':'praveen','mobile_number':'9486706677'})
    # print(users)
    return True
    
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        entryFromRequest = data['entry'][0]
        value =  entryFromRequest['changes'][0]['value']
        if('statuses' in value): 
            return jsonify({'status': 'success'}), 200
        else:
            messages = value['messages'][0]
            if(messages['type'] == 'text'):
                body_of_text = messages['text']['body']
                answer=generate_answer(body_of_text)
                url = os.getenv('base_url') + '/messages'
                headers = {
                    'Authorization': f'Bearer {os.getenv('AUTHTOKEN')}',
                    'Content-Type': 'application/json'
                }
                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": messages['from'],
                    "type": "text",
                    "text": {
                        "body": answer
                    }
                }

                response = requests.post(url, headers=headers, json=data)
                return jsonify({'status': 'success'}), 200
            else:
                body_of_text = messages['image']
                id_image = body_of_text['id']
                url = os.getenv('image_url') + id_image + '/'
                headers = {'Authorization': f'Bearer {os.getenv('AUTHTOKEN')}'}

                response = requests.get(url, headers=headers)
                response_content_str = response.content.decode('utf-8')
                response_data = json.loads(response_content_str)
                image_url = response_data['url']
                image_download = requests.get(image_url.replace("\\/", "/"),headers=headers) 

                if image_download.status_code == 200:
                    if not os.path.exists(f'{os.getenv('DOWNLOAD_DIRECTORY')}/{id_image}'):
                        os.makedirs(os.getenv('DOWNLOAD_DIRECTORY') + '/' + id_image)
                        print("Folder created successfully.")
                    else:
                        print("Folder already exists.")
                    with open(f'{os.getenv('DOWNLOAD_DIRECTORY')}/{id_image}/{id_image}.jpg', 'wb') as f:
                        f.write(image_download.content)
                        print("Media file downloaded successfully.")
                else:
                    print("Failed to download media file. Status code:", image_download.status_code)
                answer=image_details(f'{os.getenv('DOWNLOAD_DIRECTORY')}/{id_image}/{id_image}.jpg')
                url = os.getenv('base_url') + '/messages'
                headers = {
                    'Authorization': f'Bearer {os.getenv('AUTHTOKEN')}',
                    'Content-Type': 'application/json'
                }
                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": messages['from'],
                    "type": "text",
                    "text": {
                        "body": answer
                    }
                }

                response = requests.post(url, headers=headers, json=data)
                return jsonify({'status': 'success'}), 200


    elif request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
    
        if mode == 'subscribe' and token == os.getenv('verifyToken'):
            return challenge, 200
        else:
            return 'Verification failed', 403
         
     
if __name__ == '__main__':
    if not os.path.exists(os.getenv('DOWNLOAD_DIRECTORY')):
        os.makedirs(os.getenv('DOWNLOAD_DIRECTORY'))
        print("Folder created successfully.")
    else:
        print("Folder already exists.")
    app.run(host='0.0.0.0', debug=False, port=8000) 