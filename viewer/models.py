import re
import sqlite3
import tweepy
import pandas as pd
from django.db import models

from tangent.settings import DATABASES


class TweetFetcher:
    def __init__(self, **config):
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token_key'], config['access_token_secret'])
        self._api = tweepy.API(auth)

    def search(self, query):
        statuses = self._api.search(query + " -filter:retweets")
        return statuses


class UserFetcher:
    def __init__(self, **config):
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token_key'], config['access_token_secret'])
        self._api = tweepy.API(auth)

    def fetch_user(self, user_ids):
        df_users = pd.DataFrame()
        df_users.index.name = 'user_id'
        for user_id in user_ids:
            user_status = self._api.get_user(user_id)
            df_users.loc[user_id, 'name'] = user_status.name
            df_users.loc[user_id, 'screen_name'] = user_status.screen_name
            df_users.loc[user_id, 'friends_count'] = user_status.friends_count
            df_users.loc[user_id, 'followers_count'] = user_status.followers_count
            latest_tweet_statuses = self._api.user_timeline(id=user_id, count=100, include_rts=True)
            latest_tweets = ''.join([s.text for s in latest_tweet_statuses])
            df_users.loc[user_id, 'latest_tweets'] = re.sub(r'[\s,.：-＠§-　]', '', latest_tweets)
        db = sqlite3.connect(DATABASES['users']['NAME'])
        df = pd.read_sql_query("SELECT * from users;", db, index_col='user_id')
        df_users = df_users.append(df).drop_duplicates()
        df_users.to_sql("users", db, if_exists="replace")
