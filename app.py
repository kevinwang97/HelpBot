import os
from flask import Flask, request, redirect
import twilio.twiml
from twilio import twiml
# from twilio.rest import Client

app = Flask(__name__)
# app.config.from_pyfile('local_settings.py')

@app.route("/", methods=['GET', 'POST'])
def receiveAndRespond():
	sender = request.values.get('From')
	request_body = request.values.get('Body')
	# put NLP here

	if request_body == None:
        return "No request"

	if request_body.lower() == 'commands':
		body = """
		To get directions:
		directions <source> <destination> <method> <when>
		"""
    elif request_body.lower() == 'directions':
        body = "blah"
	else:
		body = "Invalid command. Text 'commands' for list of all commands"

	resp = twiml.Response()
	resp.message(body)
	return str(resp)
	
if __name__ == "__main__":
	# use heroku assigned port, or use port 5000 locally
	port = int(os.getenv('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
