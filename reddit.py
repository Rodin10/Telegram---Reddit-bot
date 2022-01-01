import praw #Put the praw.ini in the project directory!
reddit = None

def init(bot_name):
    global reddit
    reddit = praw.Reddit(bot_name)

def submitSelfPost(subredditName, title, content):
    subreddit = reddit.subreddit(subredditName)
    subreddit.submit(title, content)