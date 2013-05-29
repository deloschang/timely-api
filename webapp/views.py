from django.shortcuts import render_to_response
from django.template import RequestContext

# build the api
from social_auth.models import UserSocialAuth
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
# api
from django.http import HttpResponse

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
from django.views.decorators.csrf import csrf_exempt



def home(request):
    try:
        link = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens

        print("got link")

        access_token = link['access_token']

        return render_to_response("loggedin.html", {'access_token': access_token}, RequestContext(request))

    except AttributeError:
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
        return render_to_response("loggedin.html", {'access_token': access_token}, RequestContext(request))

    except:
        return render_to_response("main.html", RequestContext(request))


# url: /api/v1/locations
@csrf_exempt
def locations(request):
    if request.method == 'POST':
        # need to reference account first
        # CODE HERE

        # sanitize and localize the JSON
        latitude = strip_tags(request.POST['latitude'])
        longitude = strip_tags(request.POST['longitude'])

        # insert reverse-geocoder here
        # CODE here

        # load into database
        # CODE here

        # if location changes by X factor, write to calendar
        # CODE here

        # return JSON response
        #{"address":"Observatory Road, Dartmouth College, Hanover, NH 03755, USA","created_at":"2013-02-13T00:30:08Z","id":1,"latitude":"43.70359","longitude":"-72.286756","updated_at":"2013-02-13T00:30:08Z"}
        payload = {'latitude':latitude, 'longitude':longitude}

        return HttpResponse(json.dumps(payload), mimetype="application/json")


    else:
        # not POST, send error or replace with 404 later
        return render_to_response("main.html", RequestContext(request))

# url: /api/v1/movies
# Scrape the Hop and list the movies 
@csrf_exempt
def movies(request):
    if request.method == 'GET':
        # create the url

        parameters = {}

        
        payload = []# result to be generated

        data = json.dumps(parameters)
        url = 'http://hop.dartmouth.edu/Online/film'
        headers = {"Content-Type": "application/json",
            'Content-Length' : len(data),
            "Referer":"http://nutrition.dartmouth.edu:8088/",
            #"Cookie":'JSESSIONID=2C6BBA00328C1C2F67794E50337D6E3A.N1TS002',
            "User-Agent":'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
            "method":"get_nutrient_label_items",
            "params": "",
            "id":25 # why static?
            }

        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)

        read =  response.read()

        parser = read.split('searchResults : [')[1];
        parser2 = parser.split('searchFilters : [')[0];

        #print parser2
        parser3 = parser2.split('],')

        for i in range(0, len(parser3) - 1):
            parser3[i] = parser3[i].strip()

            movie = parser3[i]

            if 'HOP FILM' in movie:
                result = movie.split('HOP FILM')
                #print result[1]  # movie name

                if ',' in result[1] and result[1].strip() != "":
                    check = result[1].split(',')[1]

                    if check.strip() != "":
                        time = result[1].split(',')[1].replace('"','')
                        print time.replace('"','')  # time 
                    else:
                        break


                    place = result[1].split(',')

                    try:
                        if place[16].strip() != '"' and place[15] != "Hop / DFS and Pick 6 films":
                            movie_name = place[15].replace('"','').replace('\\','')  # movie name
                            print movie_name
                            movie_place =  place[16].replace('"','')  # place
                            print movie_place

                    except:
                        break

                    paylist={}
                    paylist={'name': movie_name, 'time': time, 'place':movie_place}
                    payload.append(paylist)

                    print "==="

                else:
                    break







        # sanitize and localize the JSON
        #latitude = strip_tags(request.POST['latitude'])
        #longitude = strip_tags(request.POST['longitude'])

        # insert reverse-geocoder here
        # CODE here

        # load into database
        # CODE here

        # if location changes by X factor, write to calendar
        # CODE here

        # return JSON response
        #{"address":"Observatory Road, Dartmouth College, Hanover, NH 03755, USA","created_at":"2013-02-13T00:30:08Z","id":1,"latitude":"43.70359","longitude":"-72.286756","updated_at":"2013-02-13T00:30:08Z"}
        #payload = {'latitude':latitude, 'longitude':longitude}
        #payload = parameters

        #return HttpResponse(json.dumps(payload), mimetype="application/json")
        return HttpResponse(json.dumps(payload), mimetype="application/json")


    else:
        # not POST, send error or replace with 404 later
        return render_to_response("main.html", RequestContext(request))


def geofences(request):
    if request.method=='POST':
        # return the location from the database
        return HttpResponse('success')
