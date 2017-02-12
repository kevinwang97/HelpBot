import os
from flask import Flask, request, redirect
import twilio.twiml
from twilio import twiml
# from twilio.rest import Client

app = Flask(__name__)
app.config.from_pyfile('local_settings.py')

# client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

@app.route("/", methods=['GET', 'POST'])
def receiveAndRespond():
	sender = request.values.get('From')
	request_body = request.values.get('Body')
	# put NLP here
	
	if request_body.lower() == 'help':
		body = """
		command | description
		-----------------------------------
		weather | get the current weather
		"""
	elif request_body.lower() == 'weather':
		body = "It is currently -1 degrees"
	else:
		body = "Invalid command. Text 'help' for commands"

	resp = twiml.Response()
	resp.message(body)
	return str(resp)
	
if __name__ == "__main__":
	# use heroku assigned port, or use port 5000 locally
	port = int(os.getenv('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
