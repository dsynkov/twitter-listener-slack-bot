
# Twitter Listener Bot for Slack

A Twitter listener bot that notifies your Slack channel(s) when users you're tracking mention a keyword you're interested in. Created with [**`tweepy`**](https://github.com/tweepy/tweepy) and inspired by @mattmakai's [How to Build Your First Slack Bot with Python](https://github.com/mattmakai/fullstackpython.com/blob/master/content/posts/160604-build-first-slack-bot-python.markdown) and Adil Moujahid's [An Introduction to Text Mining using Twitter Streaming API and Python](http://adilmoujahid.com/posts/2014/07/twitter-analytics/).

## Getting Started

To get started you'll need to create a Slack bot ("Custom Integration") and a Twitter app to get your authentication tokens. There's many ways to set up authentication. What I'll use here is a shell script (`source.sh` included as template) to export your tokens as environment variables, to be later called into the script using `os.environ.get()`. Once you have your authentication tokens for *both* Twitter and Slack, pass them into the below `source.sh` file:

**For Twitter...**

`export CONSUMER_KEY="YOUR CONSUMER_KEY HERE"`

`export CONSUMER_SECRET="YOUR CONSUMER_SECRET HERE"`

`export ACCESS_TOKEN="YOUR ACCESS_TOKEN HERE"`

`export ACCESS_TOKEN_SECRET="YOUR ACCESS_TOKEN_SECRET HERE"`

`export OWNER="YOUR SCREEN NAME HERE"`

`export OWNER_ID="YOUR OWNER_ID HERE"`

**And for Slack...**

`export SLACK_BOT_TOKEN="YOUR SLACK_BOT_TOKEN HERE"`

`export SLACK_BOT_ID="YOUR SLACK_BOT_NAME HERE"`

You can select whatever name you want when you create the bot as a Slack "Custom Integration".

Then simply import the required packages (`tweepy` and `slackclient`) with:

`$ pip install -r requirements.txt`

## Setting the Search Parameters

Configure the two files in the `static` sub-directory to set your search parameters:

1. In **`/static/users.csv`** you'll need to pass a list of Twitter accounts you want to follow. Note that these *must* be Twitter IDs and not screen names. As an example, I've selected the 581 members in Bloomberg's [Bloomberg Journalists](https://twitter.com/business/lists/bloomberg-journalists?lang=en) public Twitter list.
2. In **`/static/keywords.csv`** you'll need pass a list of keywords you want to track. This can be anything from handles, hashtags, strings, etc. You can use quotes, double quotes, or no quotes at all, insofar as they're oranized in a single column. For a timely example, I've selected keywords pertaining to Tesla's Roadster & Semi announcement, namely `'tesla','semi','elon','musk','roadster','electric car','model 3','model x'`.


## Running the Bot

After configuring your bot (I've named mine `alertbot`; you can chose any name you want) invite it into your Slack channel. The bot will work in multiple channels, but not in direct conversations.

![Alt text](/screenshots/invite.png?raw=true "Invite")

Now, the actual bot commands are in the `alertbot.py` while the Twitter listener is in `listener.py`. After selecting your `users` and `keywords` in the respective **`/static`** sub-directory files, run the following command from your terminal.

`$ python listener.py`

The bot should now be up and running. If a Tweet from one of your selected users matches your keyword criteria, you should receive a similar notification as below. (In this instance, user **@lildresodmg1** tweeted the keywords `'tesla','semi'` and `'roadster'`.) You can customize the alert message by editing the `Alertbot()` class's `self.template` attribute in `alertbot.py`.

![Alt text](/screenshots/message.PNG?raw=true "Invite")
