from slackclient import SlackClient
from datetime import datetime
import glob
import time
import os

class Alertbot:
    
    def __init__(self):
        
        self.SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
        self.SLACK_BOT_NAME = os.environ.get('SLACK_BOT_NAME')

        global sc
        sc = SlackClient(self.SLACK_BOT_TOKEN)
        
        self.SLACK_BOT_ID = self.get_bot_id()
        self.users = self.get_users()
        self.keywords = self.get_keywords()
          
        self.template = '''
Hey there! User *@{}* tweeted about {} on {} at {}: \n 
"{}" \n 
View the full URL here: \n 
{} 
'''
    
    def get_timestamp(self):

        current_time = time.time()

        date = datetime.fromtimestamp(
            current_time).strftime('%A, %b. %d')

        hour = datetime.fromtimestamp(
            current_time).strftime('%I:%M %p')

        return [date,hour]

    def get_bot_id(self):
    
        users = sc.api_call('users.list')
        members = users['members']

        for member in members:
            if member['name'] == self.SLACK_BOT_NAME:
                return member['id']
        
    def get_users(self):

        filepath = os.getcwd() + '\\static\\users.csv'

        users_file = open(filepath,'r')
        users = users_file.read().splitlines()       
        users_file.close()

        users = [user.strip('"') for user in users]
        users = [user.strip("'") for user in users]

        return users
        
    def get_keywords(self):
    
        filepath = os.getcwd() + '\\static\\keywords.csv'

        keywords_file = open(filepath,'r')
        keywords = keywords_file.read().splitlines()
        keywords_file.close()
        
        keywords = [word.strip('"') for word in keywords]
        keywords = [word.strip("'") for word in keywords]
        
        return keywords
    
    def get_bot_channels(self):

        channels = sc.api_call(
            'channels.list',
            exclude_archived=1
        )
        
        channels_list = channels['channels']

        memberships = []
        
        for channel in channels_list:
            if self.SLACK_BOT_ID in channel['members']:
                memberships.append(channel['id'])
                
        return memberships
    
    def parse_listener_output(self,tweet,content):

        if any(word.lower() in content.lower() for word in self.keywords):

            # Retrieve essentials
            user = tweet['user']
            screen_name = user['screen_name']
            timestamp = self.get_timestamp()

            # Create the tweet url
            base = 'https://twitter.com/'
            url = base + screen_name + '/status/' + str(tweet['id'])

            # Find which keyword was picked up
            matches = []
            for word in self.keywords:
                if word.lower() in content.lower():
                    matches.append(word)
            
            # Craft alert message
            alert_message = self.template.format(
                screen_name,
                matches,
                timestamp[0],
                timestamp[1],
                content,
                url
            )

            return alert_message
    
    def post_message(self,message):
        
        channels = self.get_bot_channels()
        timestamp = self.get_timestamp()
        
        for channel in channels:
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=message,
                as_user=True
            )
            
        print('Success! Message posted to {} channel(s) on {} at {}.'.format(
            len(channels),
            timestamp[0],
            timestamp[1]
            ))