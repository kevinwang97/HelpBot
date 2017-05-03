# HelpBot
A messenging bot that allows users without data to use google maps.
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