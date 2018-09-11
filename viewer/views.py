import re
import bs4
import requests
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.conf import settings

from viewer.models import TwitterSearcher
from viewer.config import config
from viewer.forms import SearchForm


def home(request):
    form = SearchForm(request.GET)
    resp = {'form': form}
    if 'target' in request.GET:
        searcher = TwitterSearcher(**config)
        statuses = searcher.search(request.GET['target'])
        tweets = [(s.created_at, s.user.screen_name, s.user.profile_image_url, s.text) for s in statuses]
        resp['tweets'] = tweets
    return render(request, 'result.html', resp)
