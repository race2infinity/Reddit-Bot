# 🤖 Making a Reddit Bot using Python and Heroku

This repo teaches you how to:

+ Make a Reddit Bot using the [PRAW](https://praw.readthedocs.io/en/latest/) (The Python Reddit API Wrapper) Python package
+ Deploy your Reddit Bot on [Heroku](https://www.heroku.com/) - A platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud
+ Install & use [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql)

In this repo, I have made a Wordbook Bot which gives the meaning of particular word / phrase in the English / Slang language.

---

## 📝 Index
+ [Why was Wordbook Bot made?](#why_was_wordbook_bot_made)
+ [Installation](#installation)
+ [Deploying the Bot on Heroku (Platform that allows you to host your Bot)](#deploying_the_bot_on_heroku)
  + [Installing Git](#installing_git)
  + [Installing Heroku CLI](#installing_heroku_cli)
  + [Getting Started](#getting_started)
  + [Initializing a local git repository](#initializing_a_local_git_repository)
  + [Creating a Remote Heroku](#creating_a_remote_heroku)
  + [Changing your App name on Heroku](#changing_your_app_name_on_heroku)
  + [Deploying code](#deploying_code)
  + [After setting up repo on Heroku](#after_setting_up_repo_on_heroku)
  + [Running the Bot](#running_the_bot)
  + [Viewing output](#viewing_output)
+ [Installing Heroku PostgreSQL](#installing_postgres)
  + [Installing locally](#installing_postgres_locally)
  + [Using the CLI](#using_the_cli)
  + [Connecting in Python](#connecting_in_python)
+ [How to use the Bot](#how_to_use_the_application)
+ [How does the Bot work?](#how_does_the_bot_work)
+ [Why didn't the Bot notice me?](#why_didnt_the_bot_notice_me)
+ [Contributing](/.github/CONTRIBUTING.md)
+ [Acknowledgements](#acknowledgements)

## 🎈 Why was Wordbook Bot made? <a name="why_was_wordbook_bot_made"></a>
Wordbook Bot was made to help Redditors:
+ Quickly look up the meaning of an English / Slang word you see
+ Find the right meaning of an English / Slang word
+ Find examples of the use of a word in natural language

## ⚙️ Installation <a name="installation"></a>
### Running Locally <a name="running_locally"></a>
#### Clone or Download the repository
```
$ git clone https://github.com/kylelobo/Reddit-Bot.git
$ cd Reddit-Bot/Wordbook_Bot
```

#### Install Dependencies
```
$ sudo apt-get install python3.6
$ sudo apt-get install pip3
$ pip3 install praw --user
$ pip3 install requests --user
```

#### Setting up Environment Variables
An app’s environment-specific configuration should be stored in environment variables (not in the app’s source code). This lets you modify each environment’s configuration in isolation, and prevents secure credentials from being stored in version control.

💡 **Note:** Do not enter spaces before and after the "=" sign. Enter your values without the quotes (" ").

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

**💡 Note:** Do not use the export keyword here.

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

**💡 Note:** You need to logout from current user and login again so environment variables changes take place

You can check if your environment variables have been set by typing ```echo $var_name``` in terminal:
```
$ echo $reddit_username
Wordbook_Bot
```

#### Start the Bot
```
$ python3 wordbook_bot.py
```

Your bot should now be running.

## 🚀 Deploying the Bot on Heroku (Platform that allows you to host your bot) <a name="deploying_the_bot_on_heroku"></a>
1. Firstly, make an account on [Heroku](https://www.heroku.com/).
2. Make another directory and put all your python code in that, and make an empty file called ```__init__.py``` in it. 3. In your main directory, create two files: ```requirements.txt``` and ```runtime.txt```.
4. The ```requirements.txt``` file should contain output of the command ```pip freeze > requirements.txt```. If you're not using ```virtualenv```, you'll have delete all the lines with packages your code doesn't use.
5. ```Runtime.txt``` just specifies which python version for Heroku to use. Mine just has the line "python-3.6.7" in it.

Now it's time to set up your git repo to use it as a remote.

### Installing Git <a name="installing_git"></a>
```
$ sudo apt-get install git-all
```

### Installing Heroku CLI <a name="installing_heroku_cli"></a>
```
$ sudo snap install --classic heroku
```

### Verifying your installation
```
$ heroku --version
heroku/7.18.3 linux-x64 node-v10.12.0
```

### Getting Started <a name="getting_started"></a>
```
$ heroku login
Enter your Heroku credentials.
Email: kyle@example.com
Password (typing will be hidden):
Authentication successful.
```

### Initializing a local git repository <a name="initializing_a_local_git_repository"></a>
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

Your app’s code is now tracked in a local Git repository. It has not yet been pushed to any remote servers.

### Creating a Remote Heroku <a name="creating_a_remote_heroku"></a>
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

### Changing your App name on Heroku <a name="changing_your_app_name_on_heroku"></a>
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

**💡 Note:** When you rename an app, it immediately becomes available at the new corresponding ```herokuapp.com``` subdomain (```newname.herokuapp.com```) and unavailable at the old one (```oldname.herokuapp.com```).

If you use the Heroku CLI to rename an app from inside it's associated Git repository, your local Heroku remote is updated automatically. However, other instances of the repository must update the remote’s details manually.

You can run the following commands to update the remote’s details in other repository instances:
```
$ git remote rm heroku
$ heroku git:remote -a newname
```

Replace ```newname``` with the new name of the app, as specified in the ```rename``` command.

### Deploying code <a name="deploying_code"></a>
To deploy your app to Heroku, you typically use the ```git push``` command to push the code from your local repository’s ```master``` branch to your ```heroku``` remote, like so:
```
$ git push heroku master
Initializing repository, done.
updating 'refs/heads/master'
  ...
```

Code diffs, manual and auto deploys via GitHub are also possible. To use GitHub as a deployment method:
```
Heroku Dashboard > Select your App > Deploy > Deployment Method > Connect to GitHub > App connected to GitHub > Select your GitHub repo
```

Thereafter, you can deploy code from your GitHub repo. If you have a local Git repo (if you have cloned your main GitHub repo), you will have to push your code to GitHub by using:
```
$ git push origin master
```

#### Deploying from a branch besides master
If you want to deploy code to Heroku from a non-```master``` branch of your local repository (for example, ```testbranch```), use the following syntax to ensure it is pushed to the remote’s ```master``` branch:
```
$ git push heroku testbranch:master
```

### After setting up repo on Heroku <a name="after_setting_up_repo_on_heroku"></a>
Once you've got your repo set up on Heroku, there's two things you'll have to change:
1. Can't use a prop (credentials) file for username / password anymore since it's untracked in your gitignore, so you'll have to set environmental variables.
2. Heroku has an ephemeral File System, and you can't preserve generated files between runs (aka pickle caching isn't an option).

To solve 1), you'll have to set environmental variables. You can set it like this from terminal:
```
# Set heroku config/env variables
$ heroku config:set reddit_username=<your_reddit_username>
$ heroku config:set reddit_password=<your_reddit_password>
$ heroku config:set client_id=<your_client_id>
$ heroku config:set client_secret=<your_client_secret>

# Confirm they're set with this command
$ heroku config
```

And programmatically retrieve it in your code like this:
```
# Retrieve heroku env variables
reddit_username = os.environ['reddit_username']
reddit_password = os.environ['reddit_password']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
```

To solve 2), a temporary solution would be to save comments as soon as you reply to them. If a comment has been saved (use ```comment.saved``` to check), then don't reply to that comment. Else, reply to that comment and then save it. To save a comment, use:
```
comment.save()
```

This is a temporary solution because Reddit has a max cap of 1000 for the number of comments / posts you can save.

A better solution would be to use a Database to store all the comment IDs. For this, you can use one of Heroku's many data storing / caching options. While most of these add-ons are free, they need you to verify yourself - by adding a credit card to your account.

The Heroku Postgres add-on however, does not require you to verify yourself. Heroku Postgres is a reliable and powerful database based on PostgreSQL. We'll be using the Heroku Postgres as the database for our Bot.

## ⛏️ Installing Heroku PostgreSQL <a name="installing_postgres"></a>
### Installing locally <a name="installing_postgres_locally"></a>
Install Postgres via your package manager. The actual package manager command you use will depend on your distribution. The following will work on Ubuntu, Debian, and other Debian-derived distributions:
```
$ sudo apt-get install postgresql
```

The psql client will typically be installed in /usr/bin:
```
$ which psql
/usr/bin/psql
```

Start the Postgres server:
```
$ sudo systemctl start postgresql
```

Installing postgres using ```apt-get``` does not create a user role or a database.

To create a superuser role and a database for your personal user account:
```
$ sudo -u postgres createuser -s $(whoami)
```

Checking if you have correctly installed Postgres:
```
$ sudo -u postgres psql
psql (10.6 (Ubuntu 10.6-1.pgdg16.04+1))
Type "help" for help.

postgres=# 
```

### Using the CLI <a name="using_the_cli"></a>
Heroku Postgres is integrated directly into the Heroku CLI and offers many helpful commands that simplify common database tasks.

But, to use it you need to provision Heroku Postgress to your app. This can be done by:
```
Log in to Heroku > Heroku dashboard > Choose your app > Resources > Add-ons > Select Heroku Postgres > Click on Provision
```

To see all PostgreSQL databases provisioned by your application and the identifying characteristics of each (such as database size, status, number of tables, and PG version), use the ```heroku pg:info``` command:
```
$ heroku pg:info
=== DATABASE_URL
Plan:                  Hobby-dev
Status:                Available
Connections:           2/20
PG Version:            10.6
Created:               2018-11-09 17:12 UTC
Data Size:             7.8 MB
Tables:                1
Rows:                  1/10000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-clear-32269
```

To establish a ```psql``` session with your remote database, use ```heroku pg:psql```.

```psql``` is the _native PostgreSQL interactive terminal_ and is used to execute queries and issue commands to the connected database.

**💡 Note:** You must have PostgreSQL [installed on your system](#installing_postgres_locally) to use ```heroku pg:psql```.
```
$ heroku pg:psql
--> Connecting to postgresql-clear-32269
psql (10.6 (Ubuntu 10.6-1.pgdg16.04+1))
SSL connection (protocol: TLSv1.2, cipher: DHE-RSA-AES256-SHA, bits: 256, compression: off)
Type "help" for help.

wordbook-bot::DATABASE=> 
```

```pg:pull``` can be used to pull remote data from a Heroku Postgres database to a database on your local machine. The command looks like this:
```
heroku pg:pull HEROKU_POSTGRESQL_MAGENTA mylocaldb --app sushi
```

This command creates a new local database named ```mylocaldb``` and then pulls data from the database at ```DATABASE_URL``` from the app ```sushi```. To prevent accidental data overwrites and loss, the local database *must not already exist*. You will be prompted to drop an already existing local database before proceeding.

If providing a Postgres user or password for your local DB is necessary, use the appropriate environment variables like so:
```
$ PGUSER=postgres PGPASSWORD=password heroku pg:pull HEROKU_POSTGRESQL_MAGENTA mylocaldb --app sushi
```

**💡 Note:** As with all ```pg:*``` commands, you can use shorthand database identifiers here. For example, to pull data from ```HEROKU_POSTGRESQL_RED``` on the app ```sushi```, you could run ```heroku pg:pull sushi::RED mylocaldb```.

```pg:push``` pushes data from a local database into a remote Heroku Postgres database. The command looks like this:
```
$ heroku pg:push mylocaldb HEROKU_POSTGRESQL_MAGENTA --app sushi
```

This command takes the local database ```mylocaldb``` and pushes it to the database at ```DATABASE_URL``` on the app ```sushi```. To prevent accidental data overwrites and loss, the remote database must be empty. You will be prompted to ```pg:reset``` a remote database that is not empty.

Usage of the ```PGUSER``` and ```PGPASSWORD``` for your local database is also supported for ```pg:push```, just like for the ```pg:pull``` command.

Heroku Postgres has a lot more Postgres commands, you can have a look at them [here](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres).

### Connecting in Python <a name="connecting_in_python"></a>
To use PostgreSQL as your database in Python applications you will need to use the ```psycopg2``` package.
```
$ pip3 install psycopg2-binary
```

And use this package to connect to ```DATABASE_URL``` in your code.
```
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Creating a cursor (a DB cursor is an abstraction, meant for data set traversal)
cur = conn.cursor()

# Executing your PostgreSQL query
cur.execute("SELECT table_name from column_name")

# In order to make the changes to the database permanent, we now commit our changes
conn.commit()

# We have committed the necessary changes and can now close out our connection
cur.close()
conn.close()
```

#### Connecting with Django (If you are using Django)
Install the ```dj-database-url``` package using ```pip```.
```
$ pip3 install dj-database-url
```

**💡 Note:** Be sure to add ```psycopg2-binary``` and ```dj-database-url``` to your ```requirements.txt``` file as well.

Then add the following to the bottom of ```settings.py```:
```
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
```

This will parse the values of the ```DATABASE_URL``` environment variable and convert them to something Django can understand.

### Running the bot <a name="running_the_bot"></a>
At this point, your bot is not yet running. You still need to:

```Log in to Heroku > Heroku dashboard > Choose your app > Resources > Edit > Enable worker > Confirm```

**💡 Note:** The free version of Heroku gives you ```550``` hours of dyno usage each month. 

### Viewing the output <a name="viewing_output"></a>
Everything the bot prints (including stacktraces when it crashes) goes to the Heroku log, which you can view with this command:
```
heroku logs
```

However, this displays only about 100 lines. In order to view the logs in real time, use the command:
```
heroku logs -t
```

## 💭 How to use the Bot <a name="how_to_use_the_application"></a>
To use the bot, type:
```
!dict word
```
The first part, i.e. "!dict" **is not** case sensitive.

The bot will then give you the Oxford Dictionary (or Urban Dictionary; if the word does not exist in the Oxford Dictionary) definition of the word as a comment reply.

### Example: <a name="example"></a>

> !dict what is love

**Definition:**

Baby, dont hurt me~
Dont hurt me~ no more.

**Example:**

Dude1: Bruh, what is love?
Dude2: Baby, dont hurt me, dont hurt me- no more!
Dude1: dafuq?

**Source:** https://www.urbandictionary.com/define.php?term=what%20is%20love

---

<sup>Beep boop. I am a bot. If there are any issues, contact my [Master](https://www.reddit.com/message/compose/?to=PositivePlayer1&subject=/u/Wordbook_Bot)</sup>

<sup>Want to make a similar reddit bot? Check out: [GitHub](https://github.com/kylelobo/Reddit-Bot)</sup>

## 😯 How does the Bot work? <a name="how_does_the_bot_work"></a>
+ The bot first extracts the word from the comment and then fetches word definitions, part of speech, example and source from the Oxford Dictionary API.
+ If the word does not exist in the Oxford Dictionary, the Oxford API then returns a 404 response upon which the bot then tries to fetch results form the Urban Dictionary API.
+ The bot uses the Pushshift API to fetch comments, PRAW module to reply to comments and Heroku as a server.
+ The entire bot is written in Python 3.6

## ☹️ Why didn't the Bot notice me? <a name="why_didnt_the_bot_notice_me"></a>
+ Make sure you are calling the bot correctly. It is:

  ``!dict word``

  The first part, i.e. "!dict" **is not** case sensitive.

+ The bot may be down due to maintenance. But, I'll try to keep the down-time as low as possible
+ I might have ran out of dynos for the month ;__;

## 🎉 Acknowledgements <a name = "acknowledgements"></a>
1. [How To Make A reddit Bot](https://www.youtube.com/watch?v=krTUf7BpTc0) - _busterroni11_
2. [A crash course in setting up your Python Reddit bot on Heroku](https://gist.github.com/ZacSweers/8595628) - _ZacSweers_
3. [Deploying with Git](https://devcenter.heroku.com/articles/git) - _Heroku_
4. [Tutorial - Create a reddit bot with python and Heroku ](http://amertune.blogspot.com/2014/04/tutorial-create-reddit-bot-with-python.html) - _amertune_
5. [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) - _Heroku_
