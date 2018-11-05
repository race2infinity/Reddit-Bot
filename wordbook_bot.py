import praw
import time
import os.path
import requests
import json
import credentials
import bot_login
import get_saved_comments

def reply_to_comment(comment, comment_reply):
    comment.reply(comment_reply)
    print ("Replied to comment \"" + comment.body + "\"\n")
    comments_replied_to.append(comment.id)

def run_bot(r, comments_replied_to):
    comment_limit = 25
    print ("Fetching first", comment_limit, "comments..\n")

    for comment in r.subreddit('test').comments(limit = comment_limit):
        try:
            if ("!Dict" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me()):
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

                    comment_reply = "\n\n>" + word_id

                    if (len(lexicalCategory) > 0):
                        comment_reply += "\n\n\n\n**Part of speech:** *" + lexicalCategory + "*"

                    if (len(definition) > 0):
                        comment_reply += "\n\n\n\n**Definition:** " + definition

                    if (len(example) > 0):
                        comment_reply += "\n\n\n\n**Example:** " + example

                    if (len(definition) > 0):
                        source = "https://en.oxforddictionaries.com/definition/" + word_id.replace(" ", "_")
                        comment_reply += "\n\n\n\n**Source:** " + source

                    comment_reply += "\n\n\n\n***\n\n*Beep bop. I am a bot. Want to make a similar reddit bot? Check out: [GitHub](https://github.com/kylelobo/Reddit-Bot)*"

                    reply_to_comment(comment, comment_reply)

                    with open ("/home/kyle/Wordbook_Bot/comments_replied_to.txt", "a+") as f:
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

                        try:
                            definition = data["list"][0]["definition"].replace("[", "").replace("]", "")
                        except:
                            definition = ""

                        try:
                            example = data["list"][0]["example"].replace("[", "").replace("]", "")
                        except:
                            example = ""

                        comment_reply = "\n\n>" + word_id

                        if (len(definition) > 0):
                            comment_reply += "\n\n\n\n**Definition:** " + definition

                        if (len(example) > 0):
                            comment_reply += "\n\n\n\n**Example:** " + example

                        if (len(definition) > 0):
                            source = "https://www.urbandictionary.com/define.php?term=" + word_id.replace(" ", "")
                            comment_reply += "\n\n\n\n**Source:** " + source

                        comment_reply += "\n\n\n\n***\n\n*Beep bop. I am a bot. Want to make a similar reddit bot? Check out: [GitHub](https://github.com/kylelobo/Reddit-Bot)*"

                        reply_to_comment(comment, comment_reply)

                        with open ("/home/kyle/Wordbook_Bot/comments_replied_to.txt", "a+") as f:
                            f.write(comment.id + " ")

                    # Word doesn't exist
                    else:
                        comment_reply = "Sorry, Such a word does not exist!"
                        reply_to_comment(comment, comment_reply)

        # Prolly low karma so can't comment as frequently
        except Exception as e:
            print ("")
            print (e)
            for i in str(e).split():
            	if(i.isdigit()):
                    time_remaining = int(i)
                    break
            if (time_remaining <= 10):
                time_remaining *= 60
            for i in range(time_remaining, 0, -1):
                time.sleep(1)
                print ("Retrying in", i, "seconds..")

    else:
        for i in range(5, 0, -1):
            time.sleep(1)
            print ("Couldn't find a comment. Checking again in", i, "secs..")


if __name__ == "__main__":
    r = bot_login.bot_login()
    comments_replied_to = get_saved_comments.get_saved_comments()
    print ("List of comment IDs", comments_replied_to, "\n")

    while True:
        run_bot(r, comments_replied_to)
