import os

def get_saved_comments():
    if not os.path.exists (os.getcwd() + "/comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open (os.getcwd() + "/comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split(" ")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to
