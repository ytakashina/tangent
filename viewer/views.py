import re
import bs4
import requests
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django import forms

from viewer.models import TwitterSearcher
from viewer.config import config


def home(request):
    searcher = TwitterSearcher(**config)
    results = searcher.search('キズナアイ')
    tweets = [(result.created_at, result.user.screen_name ,result.text) for result in results]
    return render(request, 'result.html', {'tweets': tweets})
