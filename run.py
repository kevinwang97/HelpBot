import os
from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
	resp = twilio.twiml.Response()
	resp.message("Hello!")
	return str(resp)
	
if __name__ == "__main__":
	port = int(os.getenv('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
