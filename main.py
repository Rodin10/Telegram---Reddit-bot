import time
import telegram
import json
import reddit

conf_file = open ("conf.txt", "r")
conf_lines = conf_file.readlines()
reddit_token = None
telegram_token = None
refresh_time = 300 #in seconds
previous_id = 0
subreddit = None
bot_name = None
footer = None
bot_footer = "\n\n*I'm a bot, this action was performed automatically.*"
to_forward_chat = None

for line in conf_lines: #Read conf file lines
    if "telegram" in line: #If it's the Telegram conf
        telegram_token = line.split("=")[1].rstrip("\n").strip() #remove any spaces and new line characters
    if "subreddit" in line:
        subreddit = line.split("=")[1].rstrip("\n").strip()
    if "bot_name" in line:
        bot_name = line.split("=")[1].rstrip("\n").strip()
    if "footer" in line:
        footer = line.split("=")[1].strip()
    if "to_forward_chat" in line:
        to_forward_chat = line.split("=")[1].strip()

starttime = time.time()
while True:
    print("Retrieve Telegram updates now")
    time.sleep(refresh_time - ((time.time() - starttime) % refresh_time)) 

    response = telegram.getUpdates(telegram_token, previous_id)
    result = response["result"]
    if(len(result) > 0):
        for update in response["result"]: #Get the updates from the result array
            update_id = update["update_id"]
            previous_id = update_id + 1 #Increase the previous_id by 1 to clear the updates if necessary

            try:
                message = update["channel_post"] #Only do something with channel posts
                update_text = message["text"]
                message_id = message["message_id"]
                chat_id = message["chat"]["id"]
                try:
                    entities = message["entities"]
                    if(len(entities) > 0): #Check if there are any entities
                        for entity in entities:
                            try:
                                type = entity["type"]
                                if(type == "url"): #Format the url differently so that it's clickable on Reddit
                                    offset = entity["offset"]
                                    length = entity["length"]
                                    url = update_text[offset:offset + length]
                                    update_text = update_text.replace(url, "[{0}]({0})".format(url))
                            except:
                                pass
                except Exception as exception:
                    pass
                title = update_text.split("\n")[0]
                update_text = update_text + bot_footer if footer == None else update_text + "\n\n{0}{1}".format(footer, bot_footer) #If a footer was configured add it to the post.
                reddit.init(bot_name)
                reddit.submitSelfPost(subreddit, title, update_text)
        
                if(to_forward_chat != None):
                    telegram.forwardMessage(telegram_token, to_forward_chat, chat_id, message_id)
                    
            except Exception as exception:
                pass
