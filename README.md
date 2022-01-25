# Telegram---Reddit-bot
Retrieves messages from Telegram announcement channels and posts them to specific Reddit subreddits.  

[PRAW](https://github.com/praw-dev/praw) is required!  
A conf textfile with at least the following settings is required:
- allowed_chat_usernames_or_ids (A list of whitelisted channel usernames or ids, in square brackets separated with commas, with identifiers separate by a colon i.e. [1:channel_a, 2:12345]) **The identifiers here are the basis for the other conf lines, messages retrieved from the channel with identifier 1 will be posted to the subreddit with the corresponding identifier, with the corresponding footer and to the corresponding Telegram channel if configured. These identifiers are always required, even if you only have one entry in your lists.** 
- telegram_token (Your bot token on Telegram)
- subreddits (A list of subreddits you wish to post on, in square brackets separated with commas, with identifiers separate by a colon i.e. [1:askreddit, 2:pics])
- bot_name (The name of the bot settings in praw.ini)  

If you wish you can add these setting as well:
- footers (A list of footers, in square brackets separated with commas, with identifiers separate by a colon i.e.[1:This message was brought to you by Telegram. 2:Source: Telegram] only one will appear before the "I'm a bot text" in the posts on Reddit)  
- to_forward_chats (A list of Telegram channels that the bot will forward messages to, in square brackets separated with commas, with identifiers separate by a colon i.e. [1:channel_a, 2:12345]. This will allow the bot to forward messages to the specified Telegram channels **The bot has to be an admin in the specified channel to be able to forward messages**)

All settings are supposed to be set as foo = bar.
