from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from alertbot import Alertbot
import json
import os
import time

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
OWNER = os.environ.get('OWNER')
OWNER_ID = os.environ.get('OWNER_ID')

class StdOutListener(StreamListener):
    
    def get_timestamp(self):
        
        current_time = time.time()
        current_timestamp = datetime.fromtimestamp(
            current_time).strftime('%Y-%m-%d %H:%M:%S')
        
        return current_timestamp
    
    def on_data(self, data):
        
        tweet = json.loads(data)
        
        if 'text' in tweet.keys():
            content = tweet['text']
            alert_message = bot.parse_listener_output(tweet,content)
        
        if alert_message:
        
            bot.post_message(alert_message)
        
            print(alert_message)

    def on_error(self,status):
        print(status)
        
if __name__ == '__main__':
    
    bot = Alertbot()
    
    l = StdOutListener()
    
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    
    stream.filter(follow=bot.users)