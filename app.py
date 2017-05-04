import os
from flask import Flask, request, redirect
from twilio import twiml
import sys

from datetime import datetime

sys.path.insert(0, 'HelpBot/')

from GoogleMaps import GoogleMaps
from MessageParser import MessageParser

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def receive_and_respond():
    sender = request.values.get('From')
    if request.values.get('Body') == None:
        return "No Message"
    request_body = request.values.get('Body').lower()

    message_parser = MessageParser()

    if request_body == 'commands':
        body = """
        To get directions:
        <method> directions from <origin> to <destination> <'depart at' or 'arrive by'> <when>
        """
    elif 'directions' in request_body:
        parameters = message_parser.parse_directions(request_body)
        print parameters
        gmaps = GoogleMaps(os.environ['GOOGLE_MAPS_API_KEY'])
        if parameters['time_modifier'].lower() == 'depart at':
            directions = gmaps.get_directions(origin=parameters['origin'], destination=parameters['destination'],
                                              mode=parameters['mode'], departure_time=parameters['time'])
        elif parameters['time_modifier'].lower() == 'arrive by':
            directions = gmaps.get_directions(origin=parameters['origin'], destination=parameters['destination'],
                                              mode=parameters['mode'], arrival_time=parameters['time'])
        body = str(directions)
    else:
        body = "Invalid command. Text 'commands' for list of all commands"

    resp = twiml.Response()
    resp.message(body)
    return str(resp)


if __name__ == "__main__":
    # use heroku assigned port, or use port 5000 locally
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
