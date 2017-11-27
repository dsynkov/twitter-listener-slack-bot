from slackclient import SlackClient
from datetime import datetime
import pathlib
import time
import os
import sys

import sqlutils

class Alertbot:
    
    def __init__(self):
        
        self.SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
        self.SLACK_BOT_NAME = os.environ.get('SLACK_BOT_NAME')
        
        self.sc = SlackClient(self.SLACK_BOT_TOKEN)
        
        self.SLACK_BOT_ID = self.get_bot_id()
        self.users = self.get_users()
        self.keywords = self.get_keywords()
        self.channels = self.get_bot_channels()
          
        self.slack_template = '''
Hey there! User *@{}* tweeted about {} on {} at {}: \n 
"{}" \n 
View the full URL here: \n 
{} 
'''
    
    def get_tweet_timestamp(self):

        current_time = time.time()

        date = datetime.fromtimestamp(
            current_time).strftime('%A, %b. %d')

        hour = datetime.fromtimestamp(
            current_time).strftime('%I:%M %p')

        return [date,hour]
    
    def get_db_timestamp(self):

        current_time = time.time()

        date = datetime.fromtimestamp(
            current_time).strftime('%Y-%m-%d-%I-%M-%S')

        return date
        
    def get_iso_timestamp(self):
        
        current_time = time.time()
        iso_timestamp = datetime.fromtimestamp(
            current_time).strftime('%Y-%m-%d %H:%M:%S')
        
        return iso_timestamp
    
    def get_db_filepath(self):
        
        timestamp = self.get_db_timestamp()
        
        path = pathlib.PurePath(os.getcwd())
        
        db_filepath = path / 'db' / 'alerts-{}.db'.format(timestamp) 
        
        return str(db_filepath)

    def get_bot_id(self):
    
        users = self.sc.api_call('users.list')
        members = users['members']

        for member in members:
            if member['name'] == self.SLACK_BOT_NAME:
                return member['id']
        
    def get_users(self):
        
        path = pathlib.PurePath(os.getcwd())
        filepath = path / 'static' / 'users.csv'

        users_file = open(filepath,'r')
        users = users_file.read().splitlines()       
        users_file.close()

        users = [user.strip('"') for user in users]
        users = [user.strip("'") for user in users]

        return users
        
    def get_keywords(self):
    
        path = pathlib.PurePath(os.getcwd())
        filepath = path / 'static' / 'keywords.csv'

        keywords_file = open(filepath,'r')
        keywords = keywords_file.read().splitlines()
        keywords_file.close()
        
        keywords = [word.strip('"') for word in keywords]
        keywords = [word.strip("'") for word in keywords]
        
        return keywords
    
    def get_bot_channels(self):

        channels = self.sc.api_call(
            'channels.list',
            exclude_archived=1
        )
        
        channels_list = channels['channels']

        memberships = []
        
        for channel in channels_list:
            if self.SLACK_BOT_ID in channel['members']:
                memberships.append(channel['id'])
                
        return memberships
    
    def parse_matches(self,content):
        
        # Find out which keywords were picked up
        matches = []
        for word in self.keywords:
            if word.lower() in content.lower():
                matches.append(word)
                
        return matches
    
    def count_matches(self, matches):
        # Count number of keywords picked up
        return len(matches)
    
    def parse_listener_output(self,tweet,content):

        if any(word.lower() in content.lower() for word in self.keywords):

            # Retrieve essentials
            user = tweet['user']
            screen_name = user['screen_name']
            timestamp = self.get_tweet_timestamp()

            # Create the tweet url
            base = 'https://twitter.com/'
            url = base + screen_name + '/status/' + str(tweet['id'])

            # Find which keyword was picked up
            matches = self.parse_matches(content)
            
            # Get count of matches picked up
            matches_count = self.count_matches(matches)
            
            # Craft alert message
            alert_message_slack = self.slack_template.format(
                screen_name,
                matches,
                timestamp[0],
                timestamp[1],
                content,
                url
            )
            
            if len(sys.argv) > 1:
                if sys.argv[1] == '-db':
                
                    # Get datetime var to use as PK for db 
                    iso_timestamp = self.get_iso_timestamp()
                
                    # Flatten list to avoid any confusion w/ double or single quotes
                    matches_string = ''.join(str(match) for match in matches)
                    
                    alert_message_db = (
                        tweet['id'],
                        iso_timestamp,
                        screen_name,
                        matches_string,
                        matches_count,
                        timestamp[0],
                        timestamp[1],
                        content,
                        url
                    )

                    return (alert_message_slack,alert_message_db)
            else:
                return alert_message_slack
    
    def post_message(self,message):
        
        channels = self.channels
        timestamp = self.get_tweet_timestamp()
        
        for channel in channels:
            self.sc.api_call(
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