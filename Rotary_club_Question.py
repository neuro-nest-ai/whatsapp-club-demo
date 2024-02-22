import requests


def pdf_questions(Question):
    headers = {
    'x-api-key': 'sec_Zq8An2X9CLtXA7et954k1wnKmaCZcJ3Y',
    "Content-Type": "application/json",}
    data = {
    'sourceId': "src_JpLs59QPJliUp8Q0ZwSQs",
    'messages': [
        {
            'role': "user",
            'content':Question,}]}
    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)
    if response.status_code == 200:
        if "I'm sorry" not in response.json()['content']:
             return str(response.json()['content'])
        else:
             return str("I am not answer")
    else:
        return response.status_code and str("it si error")