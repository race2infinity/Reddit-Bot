# Reddit Bot
This repo will teach you how to make a Reddit Bot using the [PRAW (The Python Reddit API Wrapper)](https://praw.readthedocs.io/en/latest/) Python package. <br>
In this repo, I'll be making a dictionary bot which gives the meaning of particular word/phrase in the English language.

# Index
+ [Installation](#installation)
+ [Deploying the Bot on Heroku (Platform that allows you to host your bot)](#deploying_the_bot)
+ [How to use the Bot](#how_to_use_the_application)

## Installation<a name="installation"></a>
### Running Locally
1. Clone or Download the repository
```
  $ git clone https://github.com/kylelobo/Reddit-Bot
  $ cd Reddit-Bot/Wordbook_Bot
```
2. Install Dependencies
```
  $ sudo apt-get install python3.6
  $ sudo apt-get install pip
  $ pip install praw --user
  $ pip install requests --user
```
3. Start the Bot
```
  $ python3 wordbook_bot.py
```
Your bot should now be running.


### Deploying the Bot on Heroku (Platform that allows you to host your bot)<a name="deploying_the_bot"></a>



### How to use the Bot<a name="how_to_use_the_application"></a>
!dict word <br>
<i>or</i> <br>
!Dict word
