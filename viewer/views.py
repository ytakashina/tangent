import re
import bs4
import requests
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.conf import settings

from viewer.models import TweetFetcher, UserFetcher
from viewer.config import config
from viewer.forms import SearchForm

tweet_fetcher = TweetFetcher(**config)
user_fetcher = UserFetcher(**config)


def home(request):
    form = SearchForm(request.GET)
    resp = {'form': form}
    if 'target' in request.GET:
        statuses = tweet_fetcher.search(request.GET['target'])
        user_ids = set([s.user.id for s in statuses])
        user_fetcher.fetch_user(user_ids)
        tweets = [(s.created_at, s.user.screen_name, s.user.profile_image_url, s.text) for s in statuses]
        resp['tweets'] = tweets
    return render(request, 'result.html', resp)
