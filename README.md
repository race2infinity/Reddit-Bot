# Reddit Bot
This repo will teach you how to make a Reddit Bot using the [PRAW](https://praw.readthedocs.io/en/latest/) (The Python Reddit API Wrapper) Python package. <br>
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
Firstly, make an account on [Heroku](https://www.heroku.com/) <br><br>
Make another directory and put all your python code in that, and make an empty file called ```__init__.py``` in it. In your main directory, create two files: "requirements.txt" and "runtime.txt".<br> The requirements.txt file should contain output of the command "pip freeze > requirements.txt". If you're not using virtualenv, you'll have to go and delete all the lines with packages your code doesn't use.<br> Runtime.txt just specifies which python version for Heroku to use. Mine just has the line "python-3.6.6" in it. <br><br>
Now it's time to set up your git repo to use it as a remote.
### Installing Git
```
  $ sudo apt-get install git-all
```
### Installing Heroku CLI
```
  $ sudo snap install --classic heroku
```
### Verifying your installation
```
  $ heroku --version
  heroku/7.18.3 linux-x64 node-v10.12.0
```
### Getting Started
```
  $ heroku login
  Enter your Heroku credentials.
  Email: kyle@example.com
  Password (typing will be hidden):
  Authentication successful.
```
### Initializing a local Git repository
```
  # Change your directory to you base directory
  $ cd myapp
  $ git init
  Initialized empty Git repository in .git/
  $ git add .
  $ git commit -m "My first commit"
  Created initial commit 5df2d09: My first commit
  44 files changed, 8393 insertions(+), 0 deletions(-)
  create mode 100644 README
  create mode 100644 Procfile
  create mode 100644 app/controllers/source_file
  ...
```
Your app’s code is now tracked in a local Git repository. It has not yet been pushed to any remote servers.<br>
### Creating a Remote Heroku
The heroku create CLI command creates a new empty application on Heroku, along with an associated empty Git repository. If you run this command from your app’s root directory, the empty Heroku Git repository is automatically set as a remote for your local repository.
```
  $ heroku create
  Creating app... done, ⬢ thawing-inlet-61413
  https://thawing-inlet-61413.herokuapp.com/ | https://git.heroku.com/thawing-inlet-61413.git
```
You can use the git remote command to confirm that a remote named heroku has been set for your app:
```
  $ git remote -v
  heroku  https://git.heroku.com/thawing-inlet-61413.git (fetch)
  heroku  https://git.heroku.com/thawing-inlet-61413.git (push)
```
### Deploying code
```
  $ git push heroku master
  Initializing repository, done.
  updating 'refs/heads/master'
  ...
```
## How to use the Bot<a name="how_to_use_the_application"></a>
!dict word <br>
<i>or</i> <br>
!Dict word
