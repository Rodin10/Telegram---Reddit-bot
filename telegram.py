from urllib.request import urlopen
import json
import requests

def getUpdates(telegram_token, offset):
    with urlopen("https://api.telegram.org/bot{token}/getUpdates?offset={offset}".format(token = telegram_token, offset = offset)) as response: #Do a get call to the getUpdates api from Telegram
        json_response = json.load(response)
        return json_response #return the json

def forwardMessage(telegram_token, new_chat_id, from_chat_id, message_id): #Forward messages to specified Telegram groups
    url = "https://api.telegram.org/bot{token}/forwardMessage".format(token = telegram_token)
    myobj = {"from_chat_id" : from_chat_id, "chat_id" : new_chat_id, "message_id" : message_id}
    x = requests.post(url, data = myobj)
    return x.text
