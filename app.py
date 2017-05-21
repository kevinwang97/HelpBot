import os
import logging
from logging.config import fileConfig
from flask import Flask, request, redirect
from twilio import twiml
import sys

from datetime import datetime

sys.path.insert(0, 'HelpBot/')

from GoogleMaps import GoogleMaps
import pyowm
from MessageParser import MessageParser, BadMessage

import psycopg2
import os
import urlparse

fileConfig('logging_config.ini')
logger = logging.getLogger()

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def receive_and_respond():
    sender = request.values.get('From')

    logger.debug("[App] - Received request from " + sender)

    if request.values.get('Body') == None:
        logger.debug("[App] - Message was empty")
        return "No Message"

    request_body = request.values.get('Body').lower()

    message_parser = MessageParser()

    if request_body == 'commands':
        body = """
        To get directions:
        <method> directions from <origin> to <destination> <'depart at' or 'arrive by'> <when>
        """
    elif 'directions' in request_body:
        try:
            if request_body.strip() == 'directions':
                with conn.cursor() as curs:
                    curs.execute("SELECT last_gmaps_query FROM textinfo WHERE sender = %s", (sender,))
                    request_body = curs.fetchone()[0]
                    logger.debug("[app] - Google Mapsgit p last request: " + request_body)
                    if request_body is None:
                        raise BadMessage("No previous request")

            parameters = message_parser.parse_directions(request_body)
            logger.debug("[App] - Google Maps Parameters: " + str(parameters))
            gmaps = GoogleMaps(os.environ['GOOGLE_MAPS_API_KEY'])
            if parameters['time_modifier'].lower() == 'depart at':
                directions = gmaps.get_directions(origin=parameters['origin'], destination=parameters['destination'],
                                                  mode=parameters['mode'], departure_time=parameters['time'])
            elif parameters['time_modifier'].lower() == 'arrive by':
                directions = gmaps.get_directions(origin=parameters['origin'], destination=parameters['destination'],
                                                  mode=parameters['mode'], arrival_time=parameters['time'])
            body = str(directions)
            logger.debug("[App] - Google Maps Response: " + body)

            with conn.cursor() as curs:
                vals = {
                    "sender": sender,
                    "last_weather_query": "",
                    "last_gmaps_query": request_body
                }
                query = "INSERT INTO textinfo (sender, last_weather_query, last_gmaps_query) VALUES (%(sender)s, %(last_weather_query)s, %(last_gmaps_query)s) ON CONFLICT (sender) DO UPDATE SET last_gmaps_query = %(last_gmaps_query)s"
                curs.execute(query, vals)
                conn.commit()

        except Exception as e:
            logger.error("[App] - Google Maps Exception: " + str(e))
            body = "Please follow message format: <method> directions from <origin> to <destination> <'depart at' or 'arrive by'> <when>"

    elif 'weather' in request_body:
        try:
            if request_body.strip() == 'weather':
                with conn.cursor() as curs:
                    curs.execute("SELECT last_weather_query FROM textinfo WHERE sender = %s", (sender,))
                    request_body = curs.fetchone()[0]
                    logger.debug("[app] - Weather last request: " + request_body)
                    if request_body is None:
                        raise BadMessage("No previous request")

            weather_location = message_parser.parse_weather_string(request_body)
            logger.debug("[App] - Weather Location: " + weather_location['location'])
            owm = pyowm.OWM(os.environ['WEATHER_API'])
            observation = owm.weather_at_place(weather_location['location'])
            weather = observation.get_weather()
            temperature = weather.get_temperature(unit='celsius')
            location = observation.get_location()
            body = "Currently, in {}, it is {} degrees ({} degrees - {} degrees) with {}.".format(location.get_name(),
                                                                                                  temperature['temp'],
                                                                                                  temperature['temp_min'],
                                                                                                  temperature['temp_max'],
                                                                                                  weather.get_detailed_status())

            with conn.cursor() as curs:
                vals = {
                    "sender": sender,
                    "last_weather_query": request_body,
                    "last_gmaps_query": ""
                }
                query = "INSERT INTO textinfo (sender, last_weather_query, last_gmaps_query) VALUES (%(sender)s, %(last_weather_query)s, %(last_gmaps_query)s) ON CONFLICT (sender) DO UPDATE SET last_weather_query = %(last_weather_query)s"
                curs.execute(query, vals)
                conn.commit()

        except Exception as e:
            logger.error("[App] - Weather: " + str(e))
            body = "Please follow message format: weather in <location>"

        logger.debug("[App] - Weather Response: " + body)

    else:
        body = "Invalid command. Text 'commands' for list of all commands"

    resp = twiml.Response()
    resp.message(body)
    return str(resp)


if __name__ == "__main__":
    # use heroku assigned port, or use port 5000 locally
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    conn.close()
