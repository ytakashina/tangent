import re
import bs4
import requests
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.conf import settings
from django import forms


def home(request):
    return render(request, 'result.html')
