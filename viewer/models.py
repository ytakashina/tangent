import tweepy
from django.db import models


class TwitterSearcher:
    def __init__(self, **config):
        auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
        auth.set_access_token(config['access_token_key'], config['access_token_secret'])
        self._api = tweepy.API(auth)

    def search(self, query):
        return self._api.search(query + " -filter:retweets")
