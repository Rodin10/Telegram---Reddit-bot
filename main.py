import time
import telegram
import json
import reddit

reddit_token = None
telegram_token = None
refresh_time = 300 #in seconds
previous_id = 0
subreddits = []
bot_name = None
footers = []
bot_footer = "\n\n*I'm a bot, this action was performed automatically.*"
to_forward_chats = []
allowed_chat_usernames_or_ids = []
allowed_chat_usernames_or_ids_cleaned = []
flairs = []

def readConf():
    conf_file = open("conf.txt", "r", encoding="utf-8") #Open the file
    conf_lines = conf_file.readlines() #Read the lines
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
        if "footers" in line:
            global footers
            footerlines = line.split("=")[1].strip()
            footerlines = footerlines[1:-1] #Remove opening and closing brackets only as we allow urls here
            footers = footerlines.split(",")  # Create the list
        if "to_forward_chats" in line:
            global to_forward_chats
            toForwardChatLines = line.split("=")[1].strip()
            toForwardChatLines = toForwardChatLines.replace("[", "",).replace("]", "").replace(" ", "") #Get rid of spacing and the brackets
            to_forward_chats = toForwardChatLines.split(",") #Create the list
        if "flairs" in line:
            global flairs
            flairLines = line.split("=")[1].strip()
            flairLines = flairLines[1:-1]  # Remove opening and closing brackets only as we allow urls here
            flairs = flairLines.split(",")  # Create the list
        if ("allowed_chat_usernames_or_ids") in line:
            all_allowed = line.split("=")[1].strip()
            all_allowed = all_allowed.replace("[", "",).replace("]", "").replace(" ", "") #Get rid of spacing and the brackets
            global allowed_chat_usernames_or_ids
            allowed_chat_usernames_or_ids = all_allowed.split(",") #Create the list
            global allowed_chat_usernames_or_ids_cleaned
            for username_or_id in allowed_chat_usernames_or_ids:
                allowed_chat_usernames_or_ids_cleaned.append(username_or_id.split(":")[1]) #add just the names or ids without the identifiers in this list for later use

def readFromConf(list, identifier):
    for entry in list:
        if(identifier in entry):
            splittedList = entry.split(":")
            i = 1
            entryToReturn = ""
            while(i < len(splittedList)): #Add everything after the identifier to the entry we're returning
                entryToReturn = entryToReturn + splittedList[i]
                i = i + 1
            return entryToReturn
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

                if(len(allowed_chat_usernames_or_ids) != 0 and (chat_username in allowed_chat_usernames_or_ids_cleaned or str(chat_id) in allowed_chat_usernames_or_ids_cleaned)): #Check if the channel post we're going to post is from an allowed source before posting
                    conf_identifier = None #Identifier for which conf settings should be used
                    for allowed_chat_username_or_id in allowed_chat_usernames_or_ids:
                        allowed_chat_username_or_id = allowed_chat_username_or_id.split(":")
                        if(allowed_chat_username_or_id[1] == chat_username):
                            conf_identifier = allowed_chat_username_or_id[0]
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
                    footerText = readFromConf(footers, conf_identifier)
                    update_text = update_text + bot_footer if footerText == None else update_text + "\n\n{0}{1}".format(footerText, bot_footer) #If a footer was configured add it to the post.
                    reddit.init(bot_name)
                    requiredFlair = readFromConf(flairs, conf_identifier)
                    flair_id = None #flair_id is empty by default
                    subredditToPost = readFromConf(subreddits, conf_identifier)
                    if(requiredFlair != None): #Check if we require a flair to post
                        flairs = reddit.getFlairs(subredditToPost)
                        for flair in flairs:
                            if(flair["flair_text"] == requiredFlair):
                                flair_id = flair["flair_template_id"] #Find the proper id to use to post
                    reddit.submitSelfPost(subredditToPost, title, update_text, flair_id)

                    if(len(to_forward_chats) > 0):
                        for to_forward_chat in to_forward_chats:
                            if(to_forward_chat.startswith(conf_identifier)): #Only forward to chats that have the correct conf identifier
                                telegram.forwardMessage(telegram_token, to_forward_chat.split(":")[1], chat_id, message_id)

            except Exception as exception:
                print(exception)
