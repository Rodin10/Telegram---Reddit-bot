# Telegram---Reddit-bot
Retrieves messages from Telegram announcement channels and posts them to specific Reddit subreddits.


[PRAW](https://github.com/praw-dev/praw) is required!  
A conf file with at least the following settings is required:
- telegram_token (Your bot token on Telegram)
- subreddit (The subreddit you wish to post on)
- bot_name (The name of the bot settings in praw.ini)
If you wish you can add this setting as well:
- footer (this will appear before the "I'm a bot text" in the posts on Reddit)
All settings are supposed to be set as foo = bar.
