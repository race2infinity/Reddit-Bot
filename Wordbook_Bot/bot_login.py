import praw
import os

def bot_login():
    print ("Logging in..")
    try:
        r = praw.Reddit(username = os.environ['reddit_username'],
                password = os.environ['reddit_password'],
                client_id = os.environ['client_id'],
                client_secret = os.environ['client_secret'],
                user_agent = "kyle")
        print ("Logged in!")
    except:
        print ("Failed to log in!")
    return r
