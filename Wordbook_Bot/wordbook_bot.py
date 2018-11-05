import praw
import time
import os
import requests
import json
import bot_login
import get_saved_comments
import credentials

def reply_to_comment(comment, comment_reply):
    comment.reply(comment_reply)
    print ("Replied to comment \"" + comment.body + "\"\n")
    comments_replied_to.append(comment.id)

def run_bot(r, comments_replied_to):
    # Use this if you want to have a limit on the number of comments you want to read
    # comment_limit = 100
    # print ("Fetching first", comment_limit, "comments..\n")

    for comment in r.subreddit('all').stream.comments():
        try:
            if ("!dict" in comment.body.lower() and comment.id not in comments_replied_to and comment.author != r.user.me()):
                print ("Found comment with string \"!Dict\"\a")

                comment_string = list(comment.body.split())[1:]

                app_id = credentials.app_id
                app_key = credentials.app_key
                language = "en"
                word_id = " ".join(str(i) for i in comment_string)

                url = "https://od-api.oxforddictionaries.com/api/v1/entries/" + language + "/" + word_id.replace(" ", "_").lower()
                req = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})

                # Oxford Dictionary
                if (req.status_code == 200):
                    print("Oxford- Data accessed sucessfully!")

                    with open("data.json", "w+") as f:
                        json.dump(req.json(), f, sort_keys = True, ensure_ascii = False, indent = 4)

                    with open("data.json") as f:
                        data = json.load(f)

                    comment_reply = "\n\n>" + word_id

                    try:
                        definition = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0].replace("[", "").replace("]", "")
                    except:
                        definition = ""

                    try:
                        lexicalCategory = data["results"][0]["lexicalEntries"][0]["lexicalCategory"].replace("[", "").replace("]", "")
                    except:
                        lexicalCategory = ""

                    try:
                        example = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"].replace("[", "").replace("]", "")
                    except:
                        example = ""

                    if (len(lexicalCategory) > 0):
                        comment_reply += "\n\n\n\n**Part of speech:** \n\n*" + lexicalCategory + "*"

                    if (len(definition) > 0):
                        comment_reply += "\n\n\n\n**Definition:** \n\n" + definition

                    if (len(example) > 0):
                        comment_reply += "\n\n\n\n**Example:** \n\n" + example

                    if (len(definition) > 0):
                        source = "https://en.oxforddictionaries.com/definition/" + word_id.replace(" ", "_")
                        comment_reply += "\n\n\n\n**Source:** " + source

                    comment_reply += "\n\n\n\n***\n\n*Beep bop. I am a bot. If there are any issues, contact my [master](https://www.reddit.com/message/compose/?to=PositivePlayer1&subject=/u/Wordbook_Bot).*\n\n*Want to make a similar reddit bot? Check out: [GitHub](https://github.com/kylelobo/Reddit-Bot)*"

                    reply_to_comment(comment, comment_reply)

                    with open (os.getcwd() + "/comments_replied_to.txt", "a+") as f:
                        f.write(comment.id + " ")

                # Urban Dictionary
                else:
                    url = "http://api.urbandictionary.com/v0/define?term={" + word_id + "}"
                    req = requests.get(url)
                    if (req.status_code == 200):

                        print ("Urban- Data accessed succesfully!")

                        with open("data.json", "w+") as f:
                            json.dump(req.json(), f, sort_keys = True, ensure_ascii = False, indent = 4)

                        with open("data.json") as f:
                            data = json.load(f)

                        comment_reply = "\n\n>" + word_id

                        if(len(data["list"]) == 0):
                            comment_reply += "\n\nSorry, Such a word does not exist!"

                        try:
                            definition = data["list"][0]["definition"].replace("[", "").replace("]", "")
                        except:
                            definition = ""

                        try:
                            example = data["list"][0]["example"].replace("[", "").replace("]", "")
                        except:
                            example = ""

                        if (len(definition) > 0):
                            comment_reply += "\n\n\n\n**Definition:** \n\n" + definition

                        if (len(example) > 0):
                            comment_reply += "\n\n\n\n**Example:** \n\n" + example

                        if (len(definition) > 0):
                            source = "https://www.urbandictionary.com/define.php?term=" + word_id.replace(" ", "%20")
                            comment_reply += "\n\n\n\n**Source:** " + source

                        comment_reply += "\n\n\n\n***\n\n*Beep bop. I am a bot. If there are any issues, contact my [master](https://www.reddit.com/message/compose/?to=PositivePlayer1&subject=/u/Wordbook_Bot).*\n\n*Want to make a similar reddit bot? Check out: [GitHub](https://github.com/kylelobo/Reddit-Bot)*"

                        reply_to_comment(comment, comment_reply)

                        with open (os.getcwd() + "/comments_replied_to.txt", "a+") as f:
                            f.write(comment.id + " ")

                    # Word doesn't exist
                    else:
                        comment_reply = "Sorry, Such a word does not exist!"
                        reply_to_comment(comment, comment_reply)

        # Prolly low karma so can't comment as frequently
        except Exception as e:
            if (str(e).split()[0] == "RATELIMIT:"):
                for i in str(e).split():
                    if (i.isdigit()):
                        time_remaining = int(i)
                        break
                if (time_remaining <= 10):
                    time_remaining *= 60
                else:
                    time_remaining = 600

            print (str(e.__class__.__name__) + ": " + str(e))
            for i in range(time_remaining, 0, -10):
                print ("Retrying in", i, "seconds..")
                time.sleep(10)

    else:
        for i in range(10, 0, -10):
            print ("Couldn't find a comment. Checking again in", i, "secs..")
            time.sleep(10)
        print ("")

if __name__ == "__main__":
    r = bot_login.bot_login()
    comments_replied_to = get_saved_comments.get_saved_comments()
    print ("List of comment IDs", comments_replied_to, "\n")

    while True:
        run_bot(r, comments_replied_to)
