import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

import requests
from twilio.twiml.messaging_response import MessagingResponse

DOWNLOAD_DIRECTORY = 'Treasurer'

def process_image(image_url):
        filename="helloworld.png"
        with open('{}'.format(filename), 'wb') as f:
           #image_url = request.values['MediaUrl0']
           f.write(image_url.content)

        print("sucesssfull")
if __name__ == "__main__":
    # Example usage:
    image_url = 'https://api.twilio.com/2010-04-01/Accounts/AC5c770f9ab12adfc23d89befc8bebad6c/Messages/MM84431f09c4806fe764a491689c51f332/Media/ME3dc923e429820862ba6f7885815b403c'
    response=requests.get(image_url)
    #print(process_image(image_url))
    print(response)



#image_url = 'https://api.twilio.com/2010-04-01/Accounts/AC5c770f9ab12adfc23d89befc8bebad6c/4b7f0020c38db84f46b376e79ca4a920Messages/MM77c7bc924317bd99ee876b848789b018/Media/MEb118e0822a03daae1e0b2c0c67a47e03'
#account_sid = 'AC5c770f9ab12adfc23d89befc8bebad6c'
#auth_token = '4b7f0020c38db84f46b376e79ca4a920'






