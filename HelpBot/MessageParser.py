import re
from dateutil import parser
from datetime import datetime


class BadMessage(Exception):
    pass


class MessageParser():
    def __init__(self):
        pass

    def parse_directions(self, string):
        regex = "^(\w+) directions from (.+) to (.+) (depart at|arrive by) ([^ ]*)$"
        match_obj = re.match(regex, string)
        time_str = match_obj.group(5)
        if time_str.lower() == "now":
            time = datetime.now()
        else:
            try:
                time = parser.parse(time_str)
            except:
                raise BadMessage("Invalid time input")
        try:
            return {
                'mode': match_obj.group(1),
                'origin': match_obj.group(2),
                'destination': match_obj.group(3),
                'time_modifier': match_obj.group(4),
                'time': time
            }
        except:
            raise BadMessage("Must follow message format")