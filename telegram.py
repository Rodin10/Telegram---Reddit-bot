from urllib.request import urlopen
import json

def getUpdates(telegram_token, offset):
    with urlopen("https://api.telegram.org/bot{token}/getUpdates?offset={offset}".format(token = telegram_token, offset = offset)) as response: #Do a get call to the getUpdates api from Telegram
        json_response = json.load(response)
        return json_response #return the json
