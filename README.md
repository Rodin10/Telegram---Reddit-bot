# Telegram---Reddit-bot
Retrieves messages from Telegram announcement channels and posts them to specific Reddit subreddits.  

[PRAW](https://github.com/praw-dev/praw) is required!  
A conf file with at least the following settings is required:
- telegram_token (Your bot token on Telegram)
- subreddit (The subreddit you wish to post on)
- bot_name (The name of the bot settings in praw.ini)  
- allowed_chat_usernames_or_ids (A list of whitelisted channel usernames or ids, in square brackets separated with commas i.e. [channel_a, 12345])

If you wish you can add these setting as well:
- footer (this will appear before the "I'm a bot text" in the posts on Reddit)  
- to_forward_chat (This will allow the bot to forward messages to the specified Telegram channel **The bot has to be an admin in the specified channel to be able to forward messages**)

All settings are supposed to be set as foo = bar.
