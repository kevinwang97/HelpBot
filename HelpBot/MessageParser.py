import re
from dateutil import parser


class BadMessage(Exception):
    pass


class MessageParser:
    def __init__(self):
        pass

    def parse_directions(self, string):
        regex = "^(\w+) directions from (.+) to (.+) (depart at|arrive by) ([^ ]*)$"
        match_obj = re.match(regex, string)
        try:
            return {
                'mode': match_obj.group(1),
                'origin': match_obj.group(2),
                'destination': match_obj.group(3),
                'time_modifier': match_obj.group(4),
                'time': parser.parse(match_obj.group(5))
            }
        except:
            raise BadMessage()