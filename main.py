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
subreddits = []
bot_name = None
footer = None
bot_footer = "\n\n*I'm a bot, this action was performed automatically.*"
to_forward_chats = []
allowed_chat_usernames_or_ids = []

def readConf():
    for line in conf_lines: #Read conf file lines
        if "telegram" in line: #If it's the Telegram conf
            global telegram_token
            telegram_token = line.split("=")[1].rstrip("\n").strip() #remove any spaces and new line characters
        if "subreddits" in line:
            global subreddits
            subredditLines = line.split("=")[1].strip()
            subredditLines = subredditLines.replace("[", "",).replace("]", "").replace(" ", "") #Get rid of spacing and the brackets
            subreddits = subredditLines.split(",") #Create the list
        if "bot_name" in line:
            global bot_name
            bot_name = line.split("=")[1].rstrip("\n").strip()
        if "footer" in line:
            global footer
            footer = line.split("=")[1].strip()
        if "to_forward_chats" in line:
            global to_forward_chats
            toForwardChatLines = line.split("=")[1].strip()
            toForwardChatLines = toForwardChatLines.replace("[", "",).replace("]", "").replace(" ", "") #Get rid of spacing and the brackets
            to_forward_chats = toForwardChatLines.split(",") #Create the list
        if ("allowed_chat_usernames_or_ids") in line:
            all_allowed = line.split("=")[1].strip()
            all_allowed = all_allowed.replace("[", "",).replace("]", "").replace(" ", "") #Get rid of spacing and the brackets
            global allowed_chat_usernames_or_ids
            allowed_chat_usernames_or_ids = all_allowed.split(",") #Create the list

readConf()
starttime = time.time()
while True:
    print("Retrieve Telegram updates now")
    time.sleep(refresh_time - ((time.time() - starttime) % refresh_time))
    response = telegram.getUpdates(telegram_token, previous_id)
    result = response["result"]
    if(len(result) > 0):
        readConf() #Read the configuration file again if we have results
        for update in response["result"]: #Get the updates from the result array
            update_id = update["update_id"]
            previous_id = update_id + 1 #Increase the previous_id by 1 to clear the updates if necessary

            try:
                message = update["channel_post"] #Only do something with channel posts
                update_text = message["text"]
                message_id = message["message_id"]
                chat_id = message["chat"]["id"]
                chat_username = message["chat"]["username"]
                if(len(allowed_chat_usernames_or_ids) != 0 and (chat_username in allowed_chat_usernames_or_ids or str(chat_id) in allowed_chat_usernames_or_ids)): #Check if the channel post we're going to post is from an allowed source before posting
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
                    print("Posting to reddit and forwarding to Telegram now")
                    title = update_text.split("\n")[0]
                    update_text = update_text + bot_footer if footer == None else update_text + "\n\n{0}{1}".format(footer, bot_footer) #If a footer was configured add it to the post.
                    reddit.init(bot_name)
                    for subreddit in subreddits:
                        reddit.submitSelfPost(subreddit, title, update_text)

                    if(len(to_forward_chats) > 0):
                        for to_forward_chat in to_forward_chats:
                            telegram.forwardMessage(telegram_token, to_forward_chat, chat_id, message_id)
                    
            except Exception as exception:
                pass
