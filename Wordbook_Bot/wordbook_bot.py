import praw
import time
import os
import requests
import json
import bot_login
import psycopg2

def json_dump_and_parse(file_name, request):
    with open(file_name, "w+") as f:
        json.dump(request.json(), f, sort_keys = True, ensure_ascii = False, indent = 4)
    with open(file_name) as f:
        data = json.load(f)
    return data

def reply_to_comment(r, comment_id, comment_reply, dictionary_type, comment_subreddit, comment_author, comment_body):
    try:
        comment_to_be_replied_to = r.comment(id=comment_id)
        comment_to_be_replied_to.reply(comment_reply)
        print ("\nReply details:\nDictionary: {}\nSubreddit: r/{}\nComment: \"{}\"\nUser: u/{}\a". format(dictionary_type, comment_subreddit, comment_body, comment_author))

    # Probably low karma so can't comment as frequently
    except Exception as e:
        time_remaining = 15
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

def run_bot(r, created_utc, conn):
    try:
        comment_url = "https://api.pushshift.io/reddit/search/comment/?q=!dict&sort=desc&size=50&fields=author,body,created_utc,id,subreddit&after=" + created_utc

        parsed_comment_json = json_dump_and_parse("comment_data.json", requests.get(comment_url))

        if (len(parsed_comment_json["data"]) > 0):
            created_utc = parsed_comment_json["data"][0]["created_utc"]

            cur.execute("UPDATE comment_time SET created_utc = {}". format(created_utc))
            cur.execute("SELECT created_utc from comment_time")
            conn.commit()

            for comment in parsed_comment_json["data"]:

                comment_author = comment["author"]
                comment_body = comment["body"]
                comment_id = comment["id"]
                comment_subreddit = comment["subreddit"]

                if ("!dict" in comment_body.lower() and comment_author != "Wordbook_Bot"):
                    print ("\n\nFound a comment!")
                    comment_body_list = list(comment_body.split())[1:]

                    app_id = os.environ["app_id"]
                    app_key = os.environ["app_key"]
                    language = "en"

                    word = " ".join(str(i) for i in comment_body_list)

                    oxford_url = "https://od-api.oxforddictionaries.com/api/v1/entries/" + language + "/" + word.replace(" ", "_").lower()
                    request = requests.get(oxford_url, headers = {"app_id": app_id, "app_key": app_key})

                    # Oxford Dictionary
                    if (request.status_code == 200):
                        dictionary_type = "Oxford"
                        parsed_word_json = json_dump_and_parse("word_data.json", request)
                        comment_reply = "\n\n>" + word

                        try:
                            lexicalCategory = parsed_word_json["results"][0]["lexicalEntries"][0]["lexicalCategory"].replace("[", "").replace("]", "")
                            comment_reply += "\n\n\n\n**Part of speech:** \n\n*" + lexicalCategory + "*"
                        except:
                            lexicalCategory = ""

                        try:
                            definition = parsed_word_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0].replace("[", "").replace("]", "")
                            comment_reply += "\n\n\n\n**Definition:** \n\n" + definition
                        except:
                            definition = ""

                        try:
                            example = parsed_word_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"].replace("[", "").replace("]", "")
                            comment_reply += "\n\n\n\n**Example:** \n\n" + example
                        except:
                            example = ""

                        if (len(definition) > 0):
                            source = "https://en.oxforddictionaries.com/definition/" + word.replace(" ", "_")
                            comment_reply += "\n\n\n\n**Source:** " + source

                    # Urban Dictionary
                    else:
                        urban_dict_url = "http://api.urbandictionary.com/v0/define?term={" + word + "}"
                        request = requests.get(urban_dict_url)

                        if (request.status_code == 200):
                            dictionary_type = "Urban"
                            parsed_word_json = json_dump_and_parse("word_data.json", requests.get(urban_dict_url))
                            comment_reply = "\n\n>" + word

                            if(len(parsed_word_json["list"]) == 0):
                                comment_reply += "\n\nSorry, such a word does not exist!"
                                dictionary_type = "None"

                            try:
                                definition = parsed_word_json["list"][0]["definition"].replace("[", "").replace("]", "")
                                comment_reply += "\n\n\n\n**Definition:** \n\n" + definition
                            except:
                                definition = ""

                            try:
                                example = parsed_word_json["list"][0]["example"].replace("[", "").replace("]", "")
                                comment_reply += "\n\n\n\n**Example:** \n\n" + example
                            except:
                                example = ""

                            if (len(definition) > 0):
                                source = "https://www.urbandictionary.com/define.php?term=" + word.replace(" ", "%20")
                                comment_reply += "\n\n\n\n**Source:** " + source

                        # Word doesn't exist
                        else:
                            comment_reply = "\n\nSorry, such a word does not exist!"
                            dictionary_type = "None"

                    comment_reply += "\n\n\n\n---\n\n^(Beep boop. I am a bot. If there are any issues, contact my) [^Master ](https://www.reddit.com/message/compose/?to=PositivePlayer1&subject=/u/Wordbook_Bot)\n\n^(Want to make a similar reddit bot? Check out: ) [^GitHub ](https://github.com/kylelobo/Reddit-Bot)"

                    reply_to_comment(r, comment_id, comment_reply, dictionary_type, comment_subreddit, comment_author, comment_body)

                    print ("\nFetching comments..")

    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))

    return str(created_utc)

if __name__ == "__main__":
    while True:
        try:
            r = bot_login.bot_login()
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            cur = conn.cursor()
            cur.execute("SELECT created_utc from comment_time")
            created_utc = cur.fetchall()

            if (len(created_utc) > 0):
                created_utc = str(created_utc[0][0])
            else:
                created_utc = ""
            print ("\nFetching comments..")
            while True:
                # Fetching all new comments that were created after created_utc time
                created_utc = run_bot(r, created_utc, conn)
                time.sleep(10)

        except Exception as e:
            print (str(e.__class__.__name__) + ": " + str(e))
            time.sleep(15)
