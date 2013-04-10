from django.shortcuts import render_to_response
from django.template import RequestContext

# build the api
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

import json 
import httplib2

# scraper
import urllib
import urllib2
import cookielib
from html5lib import HTMLParser, treebuilders

from django.utils.html import strip_tags # sanitize

# extra
import datetime
from datetime import timedelta


def home(request):
    try: 
        link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
        access_token = link['access_token']

        return render_to_response("loggedin.html", {'access_token': access_token}, RequestContext(request))

    except:
        return render_to_response("main.html", RequestContext(request))


