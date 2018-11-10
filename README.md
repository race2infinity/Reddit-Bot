# Reddit Bot
This repo teaches you how to make a Reddit Bot using the [PRAW](https://praw.readthedocs.io/en/latest/) (The Python Reddit API Wrapper) Python package. <br>
In this repo, I have made a dictionary bot which gives the meaning of particular word/phrase in the English language.

# Index
+ [Installation](#installation)
+ [Deploying the Bot on Heroku (Platform that allows you to host your Bot)](#deploying_the_bot)
+ [How to use the Bot](#how_to_use_the_application)
+ [References](#references)

## Installation<a name="installation"></a>
### Running Locally
#### Clone or Download the repository
```
$ git clone https://github.com/kylelobo/Reddit-Bot.git
$ cd Reddit-Bot/Wordbook_Bot
```
#### Install Dependencies
```
$ sudo apt-get install python3.6
$ sudo apt-get install pip
$ pip install praw --user
$ pip install requests --user
```
#### Setting up Environment Variables
An app’s environment-specific configuration should be stored in environment variables (not in the app’s source code). This lets you modify each environment’s configuration in isolation, and prevents secure credentials from being stored in version control.<br><br>
<b>Note:<br>
Do not enter spaces before and after the "=" sign.<br>
Enter your values without the quotes (" ").</b><br><br>
To set variable only for current shell:
```
VARNAME="your value"
```

To set it for current shell and all processes started from current shell:
```
export VARNAME="your value"      # shorter, less portable version
```
To set it permanently for all future bash sessions add such line to your ```.bashrc``` file in your ```$HOME``` directory.

To set it permanently, and system wide (all users, all processes) add ```set``` variable in ```/etc/environment```:
```
sudo -H gedit /etc/environment
```
This file only accepts variable assignments like:
```
VARNAME="your value"
```
Do not use the export keyword here.<br><br>
Here is the list of environment variables you need to set:
```
# Your Reddit ID & Pass
reddit_username="your_reddit_username"
reddit_password="your_reddit_password"

# Reddit API ID & Key (which you can get from here: https://www.reddit.com/prefs/apps/)
client_id="your_client_id"
client_secret="your_client_secret"

# Oxford Dictionary application ID & Key (which you can get from here: https://developer.oxforddictionaries.com/)
app_id="your_app_id"
app_key="your_app_key"
```

You need to logout from current user and login again so environment variables changes take place

#### Start the Bot
```
$ python3 wordbook_bot.py
```
Your bot should now be running.


### Deploying the Bot on Heroku (Platform that allows you to host your bot)<a name="deploying_the_bot"></a>
Firstly, make an account on [Heroku](https://www.heroku.com/) <br><br>
Make another directory and put all your python code in that, and make an empty file called ```__init__.py``` in it. In your main directory, create two files: "requirements.txt" and "runtime.txt".<br> The requirements.txt file should contain output of the command "pip freeze > requirements.txt". If you're not using virtualenv, you'll have delete all the lines with packages your code doesn't use.<br> Runtime.txt just specifies which python version for Heroku to use. Mine just has the line "python-3.6.6" in it. <br><br>
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
# Change your directory to your base directory
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
#### For a new Heroku App
The ```heroku create``` CLI command creates a new empty application on Heroku, along with an associated empty Git repository. If you run this command from your app’s root directory, the empty Heroku Git repository is automatically set as a remote for your local repository.
```
$ heroku create
Creating app... done, ⬢ thawing-inlet-61413
https://thawing-inlet-61413.herokuapp.com/ | https://git.heroku.com/thawing-inlet-61413.git
```
You can use the ```git remote``` command to confirm that a remote named ```heroku``` has been set for your app:
```
$ git remote -v
heroku  https://git.heroku.com/thawing-inlet-61413.git (fetch)
heroku  https://git.heroku.com/thawing-inlet-61413.git (push)
```
#### For an existing Heroku App
If you have already created your Heroku app, you can easily add a remote to your local repository with the ```heroku git:remote``` command. All you need is your Heroku app’s name:
```
$ heroku git:remote -a thawing-inlet-61413
set git remote heroku to https://git.heroku.com/thawing-inlet-61413.git
```

### Changing your App name on Heroku
You can rename an app at any time with the ```heroku apps:rename command```. For example, to rename an app named “oldname” to “newname”, run the ```heroku apps:rename``` command from your app’s Git repository:
```
$ heroku apps:rename newname
Renaming oldname to newname... done
http://newname.herokuapp.com/ | git@herokuapp.com:newname.git
Git remote heroku updated
```
You can also rename an app from outside of its associated Git repository by including the ```--app``` option in the command:
```
$ heroku apps:rename newname --app oldname
http://newname.herokuapp.com/ | git@herokuapp.com:newname.git
```
When you rename an app, it immediately becomes available at the new corresponding ```herokuapp.com``` subdomain (```newname.herokuapp.com```) and unavailable at the old one (```oldname.herokuapp.com```).

If you use the Heroku CLI to rename an app from inside it's associated Git repository, your local Heroku remote is updated automatically. However, other instances of the repository must update the remote’s details manually.

You can run the following commands to update the remote’s details in other repository instances:
```
$ git remote rm heroku
$ heroku git:remote -a newname
```
Replace ```newname``` with the new name of the app, as specified in the ```rename``` command.

### Deploying code
To deploy your app to Heroku, you typically use the ```git push``` command to push the code from your local repository’s ```master``` branch to your ```heroku``` remote, like so:
```
$ git push heroku master
Initializing repository, done.
updating 'refs/heads/master'
  ...
```
#### Deploying from a branch besides master
If you want to deploy code to Heroku from a non-```master``` branch of your local repository (for example, ```testbranch```), use the following syntax to ensure it is pushed to the remote’s ```master``` branch:
```
$ git push heroku testbranch:master
```
### After setting up repo on Heroku
Once you've got your repo set up on Heroku, there's two things you'll have to change:<br>
1. Can't use a prop (credentials) file for username/password anymore since it's untracked in your gitignore, so you'll have to set environmental variables.<br>
2. Heroku has it's own weird File System, and you can't preserve generated files between runs (AKA pickle caching isn't an option).<br>

To solve 1), you'll have to set environmental variables. You can set it like this from terminal:
```
# Set heroku config/env variables
$ heroku config:set reddit_username=<username>
$ heroku config:set reddit_password=<password>
$ heroku config:set client_id=<client_id>
$ heroku config:set client_secret=<client_secret>

# Confirm they're set with this command
$ heroku config
```
And programmatically retrieve it in your code like this:
```
# Retrieve heroku env variables
username = os.environ['reddit_username']
password = os.environ['reddit_password']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
```

To solve 2), a temporary solution would be to save comments as soon as you reply to them. If a comment has been saved (use ```comment.saved``` to check), then don't reply to that comment. Else, reply to that comment and then save it. To save a comment, use:
```
comment.save()
```
This is a temporary solution because Reddit has a max cap of 1000 for the number of comments/posts you can save. <br>
A better solution would be to use a Database to store all the comment IDs.<br>

At this point, your bot is not yet running. You still need to ```Log in to Heroku > Heroku dashboard > Choose your app > Resources > Edit > Enable worker > Confirm```<br><br>
The free version of Heroku gives you 550 hours of dyno usage each month. 

### Viewing the output
Everything the bot prints (including stacktraces when it crashes) goes to the Heroku log, which you can view with this command:
```
heroku logs
```
However, this displays only about 100 lines. In order to view the logs in real time, use the command:
```
heroku logs -t
```

## How to use the Bot<a name="how_to_use_the_application"></a>
```
!dict word
```
The first part, i.e. "!dict" <b>is not</b> case sensitive.

## References<a name="references"></a>:
https://www.youtube.com/watch?v=krTUf7BpTc0<br>
https://gist.github.com/hzsweers/8595628<br>
https://devcenter.heroku.com/articles/git<br>
http://amertune.blogspot.com/2014/04/tutorial-create-reddit-bot-with-python.html
