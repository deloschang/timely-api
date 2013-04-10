from django.shortcuts import render_to_response
from django.template import RequestContext

# build the api
from social_auth.models import UserSocialAuth
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

def loggedin(request):
    try: 
        link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens

        access_token = link['access_token']

        # OAuth dance
        credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('calendar', 'v3', http=http)


        # Snippet that lists all calendar events
        #request = service.events().list(calendarId='primary')
        
        #while request != None:
          ## Get the next page.
          #response = request.execute()
          ## Accessing the response like a dict object with an 'items' key
          ## returns a list of item objects (events).
          #for event in response.get('items', []):
            ## The event object is a dict object with a 'summary' key.
            #print repr(event.get('summary', 'NO SUMMARY')) + '\n'
          ## Get the next request object by passing the previous request object to
          ## the list_next method.
          #request = service.events().list_next(request, response)

        #except AccessTokenRefreshError:
        ## The AccessTokenRefreshError exception is raised if the credentials
        ## have been revoked by the user or they have expired.
        #print ('The credentials have been revoked or expired, please re-run'
               #'the application to re-authorize')

        # working event
        event = {
          'summary': "summary",
          'description': "description",
          'start' : { 'dateTime' : "2013-04-01T15:00:00.000Z"},
          'end' : { 'dateTime' : "2013-04-01T17:00:00.000Z"}
        }


        #created_event = service.events().insert(calendarId='primary', body=event).execute()

        #print "Created Event: %s" % created_event['id']
        return render_to_response("loggedin.html", RequestContext(request))

    except: 
        return render_to_response("main.html", RequestContext(request))
    

# begin the api
# url: /api/v1/locations
def locations(request):
    if request.method == 'POST':
        # sanitize and localize
        latitude = strip_tags(request.POST['latitude'])
        longitude = strip_tags(request.POST['longitude'])


    else:
        # not POST, send home
        return render_to_response("main.html", RequestContext(request))


