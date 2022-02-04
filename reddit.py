import praw #Put the praw.ini in the project directory!
reddit = None

def init(bot_name):
    global reddit
    reddit = praw.Reddit(bot_name)

def submitSelfPost(subredditName, title, content, flair_id):
    subreddit = getSubreddit(subredditName)
    subreddit.submit(title, selftext=content, flair_id=flair_id)

def getFlairs(subredditName):
    flairSelect = "r/{0}/api/flairselector/".format(subredditName) #Retrieve the flairs using the Reddit API rather than praw as this function is not yet implemented in PRAW
    flairs = reddit.post(flairSelect, data={"is_newlink": True})["choices"]
    return flairs

def getSubreddit(subredditName): #Retrieve the subreddit by its name
    subreddit = reddit.subreddit(subredditName) 
    return subreddit
