import googlemaps
import re


class GoogleMaps():
    def __init__(self, api_key):
        self.api_key = api_key
        self.google_maps = googlemaps.Client(key=self.api_key)

    def get_directions(self, origin, destination,
                       mode=None, waypoints=None, alternatives=False, avoid=None,
                       language=None, units=None, region=None, departure_time=None,
                       arrival_time=None, optimize_waypoints=False, transit_mode=None,
                       transit_routing_preference=None, traffic_model=None):
        def get_default_directions(step):
            instruction = re.sub('<[^<]+?>', '', step['html_instructions'])
            return "{} (distance: {}, duration: {})".format(instruction, step['distance']['text'],
                                                              step['duration']['text'])

        def get_transit_directions(step):
            print step
            headsign = step['transit_details']['headsign']
            type = step['transit_details']['line']['vehicle']['type']
            num_stops = step['transit_details']['num_stops']
            departure_stop = step['transit_details']['departure_stop']['name']
            departure_time = step['transit_details']['departure_time']['text']
            arrival_stop = step['transit_details']['arrival_stop']['name']
            arrival_time = step['transit_details']['arrival_time']['text']
            return "Take {} (headsign: {}) from {} ({}) to {} ({}). There will be {} stops.".format(type, headsign,
                                                                                                      departure_stop,
                                                                                                      departure_time,
                                                                                                      arrival_stop,
                                                                                                      arrival_time,
                                                                                                      num_stops)

        directions = self.google_maps.directions(origin, destination, mode, waypoints, alternatives, avoid,
                                                 language, units, region, departure_time, arrival_time,
                                                 optimize_waypoints,
                                                 transit_mode, transit_routing_preference, traffic_model)

        directions_english = ""
        for (instruction_num, step) in enumerate(directions[0]['legs'][0]['steps'], start=1):
            directions_english += "{}) ".format(str(instruction_num))
            if step['travel_mode'] == 'TRANSIT':
                directions_english += get_transit_directions(step)
            else:
                directions_english += get_default_directions(step)
            directions_english += '\n'

        return directions_english
