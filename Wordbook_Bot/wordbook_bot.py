import praw
import time
import os
import requests
import json
import bot_login


def reply_to_comment(r, comment_id, comment_reply, dictionary_type, comment_subreddit, comment_author, comment_body):
    comment_to_be_replied_to = r.comment(id=comment_id)
    comment_to_be_replied_to.save()
    comment_to_be_replied_to.reply(comment_reply)
    print ("\nReply details:\nDictionary: {}\nSubreddit: r/{}\nComment: \"{}\"\nUser: u/{}\a". format(dictionary_type, comment_subreddit, comment_body, comment_author))


def run_bot(r, after_utc):
    try:
        comment_url = "https://api.pushshift.io/reddit/search/comment/?q=!dict&sort=desc&size=25&fields=author,body,id,subreddit,created_utc&after=" + after_utc
        comment_req = requests.get(comment_url)
        with open("comment_data.json", "w+") as f:
            json.dump(comment_req.json(), f, sort_keys = True, ensure_ascii = False, indent = 4)

        with open("comment_data.json") as f:
            parsed_json = json.load(f)

        if (len(parsed_json["data"]) > 0):
            after_utc = parsed_json["data"][0]["created_utc"]

            for x in parsed_json["data"]:
                try:
                    comment_author = x["author"]
                    comment_body = x["body"]
                    comment_id = x["id"]
                    comment_subreddit = x["subreddit"]
                    comment_saved = r.comment(id=comment_id)
                    if ("!dict" in comment_body.lower() and not comment_saved.saved and comment_author != "Wordbook_Bot"):
                        print ("\n\nFound a comment!")
                        comment_body_list = list(comment_body.split())[1:]

                        app_id = os.environ["app_id"]
                        app_key = os.environ["app_key"]
                        language = "en"
                        word_id = " ".join(str(i) for i in comment_body_list)

                        url = "https://od-api.oxforddictionaries.com/api/v1/entries/" + language + "/" + word_id.replace(" ", "_").lower()
                        req = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})

                        # Oxford Dictionary
                        if (req.status_code == 200):
                            dictionary_type = "Oxford"

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

                        # Urban Dictionary
                        else:
                            url = "http://api.urbandictionary.com/v0/define?term={" + word_id + "}"
                            req = requests.get(url)
                            if (req.status_code == 200):
                                dictionary_type = "Urban"

                                with open("data.json", "w+") as f:
                                    json.dump(req.json(), f, sort_keys = True, ensure_ascii = False, indent = 4)

                                with open("data.json") as f:
                                    data = json.load(f)

                                comment_reply = "\n\n>" + word_id

                                if(len(data["list"]) == 0):
                                    comment_reply += "\n\nSorry, such a word does not exist!"
                                    dictionary_type = "None"

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

                            # Word doesn't exist
                            else:
                                comment_reply = "\n\nSorry, such a word does not exist!"
                                dictionary_type = "None"

                        comment_reply += "\n\n\n\n---\n\n^(Beep boop. I am a bot. If there are any issues, contact my [master](https://www.reddit.com/message/compose/?to=PositivePlayer1&subject=/u/Wordbook_Bot).)\n\n^(Want to make a similar reddit bot? Check out: [GitHub](https://github.com/kylelobo/Reddit-Bot))"

                        reply_to_comment(r, comment_id, comment_reply, dictionary_type, comment_subreddit, comment_author, comment_body)

                        print ("\nFetching comments..")

                # Prolly low karma so can't comment as frequently
                except Exception as e:
                    time_remaining = 5
                    if (str(e).split()[0] == "RATELIMIT:"):
                        for i in str(e).split():
                            if (i.isdigit()):
                                time_remaining = int(i)
                                break
                        if (not "seconds" or not "second" in str(e).split()):
                            time_remaining *= 60

                    print (str(e.__class__.__name__) + ": " + str(e))
                    for i in range(time_remaining, 0, -5):
                        print ("Retrying in", i, "seconds..")
                        time.sleep(5)

    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))

    return str(after_utc)

if __name__ == "__main__":
    while True:
        try:
            r = bot_login.bot_login()
            after_utc = ""
            print ("\nFetching comments..")
            while True:
                after_utc = run_bot(r, after_utc)
        except Exception as e:
            print (str(e.__class__.__name__) + ": " + str(e))
