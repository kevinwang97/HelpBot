# HelpBot
HelpBot is an SMS messenging bot aimed at helping people who do not have data (or have run out of data) on their mobile device but have texting capabilities.

Currently, HelpBot has the following features (see below for examples):
* Google Maps
* Weather

HelpBot will have support for these in the future:
* Yelp
* Sports


## Sample Usage
#### Google Maps Integration
Text HelpBot:
```
Transit directions from columbia/beechlawn to 330 philip street, waterloo depart at now
```
Response:
```
1) Walk to Columbia / Beechlawn (distance: 88 m, duration: 1 min)
2) Take BUS (headsign: Conestoga Mall) from Columbia / Beechlawn (11:06pm) to Columbia / Phillip (11:10pm). There will be 2 stops.
3) Walk to 330 Phillip St, Waterloo, ON N2L 3W9, Canada (distance: 0.1 km, duration: 2 mins)
```

#### Weather
Text HelpBot:
```
Weather in waterloo
```
Response:
```
Currently, in Waterloo, it is 12.89 degrees (11.0 degrees - 15.0 degrees) with overcast clouds.
```

## Development
### Virtual Environment
```bash
$ pip install virtualenv
$ virtualenv --no-site-packages
$ source bin/activate
$ bin/pip install -r requirements.txt
```
## Start Heroku App
```bash
$ heroku login
Enter your Heroku credentials.
Email: <email>
Password: <password>
$ heroku create
$ git push heroku master
```
Set heroku environment variables:
```bash
heroku config:set GOOGLE_MAPS_API_KEY=<insert google maps api key>
heroku config:set WEATHER_API=<insert open weather api key>
```

## Configure a Twilio Number
Go to your Twilio account and add a phone number.
Then, configure the phone number so that its messaging webhook is the heroku application url. 
