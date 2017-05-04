# HelpBot
A messenging bot that gives users without cellular data an alternative to apple and google maps (though it uses google maps API).
## Virtual Environment
```bash
$ pip install virtualenv
$ virtualenv --no-site-packages
$ source bin/activate
$ bin/pip install -r requirements.txt
```
## Start the Heroku App
```bash
$ heroku login
Enter your Heroku credentials.
Email: <email>
Password: <password>
$ heroku create
$ git push heroku master
```
## Configure a Twilio Number
Go to your Twilio account and add a phone number.
Then, configure the phone number so that its messaging webhook is the heroku application url. 

## Example Usages
Text HelpBot:
```
Transit directions from columbia/beechlawn to 330 philip street, waterloo depart at now
```
Response:
```
Walk to Columbia / Beechlawn (distance: 88 m, duration: 1 min)
Take BUS (headsign: Conestoga Mall) from Columbia / Beechlawn (11:06pm) to Columbia / Phillip (11:10pm). There will be 2 stops.
Walk to 330 Phillip St, Waterloo, ON N2L 3W9, Canada (distance: 0.1 km, duration: 2 mins)
```
