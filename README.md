
Introduction
------------

This is the Timely API.

## Locations

POST `latitude` and `longitude` to
`http://mytimely.com/api/v1/locations` or
`http://localhost:8000/api/v1/locations`.

```sh
λ virtualbox timely → λ git master → curl -d 'latitude=43.70359&longitude=-72.286756' http://localhost:8000/api/v1/locations
{"address":"Observatory Road, Dartmouth College, Hanover, NH 03755, USA","created_at":"2013-02-13T00:30:08Z","id":1,"latitude":"43.70359","longitude":"-72.286756","updated_at":"2013-02-13T00:30:08Z"}
```

Setup
------
In timelyapi/settings.py, setup variables for Templates, Static, Google
Client, Google Secret

You can set up a .sh script that sources these variables for you
Example: source setup.sh

Deploy
------

TimelyApi w/ Heroku deployment. App is live [here] (http://pure-retreat-6606.herokuapp.com/)

Deploy using
```sh
git push heroku master
```
