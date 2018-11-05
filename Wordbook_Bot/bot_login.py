import praw
import os
import credentials

def bot_login():
    print ("Logging in..")
    try:
        r = praw.Reddit(username = credentials.reddit_username,
                password = credentials.reddit_password,
                client_id = credentials.client_id,
                client_secret = credentials.client_secret,
                user_agent = "kyle")
        print ("Logged in!")
    except:
        print ("Failed to log in!")
    return r
