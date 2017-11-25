from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import json
import os
import time

# Import custom packages
from alertbot import Alertbot
import sqlcommands

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
OWNER = os.environ.get('OWNER')
OWNER_ID = os.environ.get('OWNER_ID')

class StdOutListener(StreamListener):
       
    def on_data(self, data):
        tweet = json.loads(data)
        if 'text' in tweet.keys():
            content = tweet['text']
            if commit_to_db:
                try:
                    # Get both the slack and db verions of the alert message 
                    alert_message_slack, alert_message_db = bot.parse_listener_output(
                        tweet,content)
                        
                    # Commit message to db
                    sqlcommands.commit_alert(conn,alert_message_db)
                
                except TypeError:
                    pass 
                    
            else:
                # Get only the slack version of the alert message
                alert_message_slack = bot.parse_listener_output(tweet,content)
                       
        try:
            if alert_message_slack:
                # Post message to slack channel
                bot.post_message(alert_message_slack)
                # Print message to terminal 
                print(alert_message_slack)
                
        except UnboundLocalError:
            pass

    def on_error(self,status):
        print(status)
        
if __name__ == '__main__':
    
    bot = Alertbot()
    
    commit_to_db = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '-db':
        
            commit_to_db = True
        
            # Get auto-generated gb filepath 
            database = bot.get_db_filepath()
        
            # Establish sqlite db connection 
            conn = sqlcommands.create_connection(database)
            sqlcommands.create_table(database)
    
    l = StdOutListener()
    
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    
    stream.filter(follow=bot.users)