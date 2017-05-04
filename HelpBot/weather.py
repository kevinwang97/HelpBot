import requests


class InvalidWeatherAPIRequestException(Exception):
    pass


'''
Uses OpenWeather api to retrieve weather information
'''


class WeatherAPI(APIConnection):
    def __init__(self):
        super(WeatherAPI, self).__init__("http://api.openweathermap.org/data/2.5")

    def getWeather(self, **kwargs):
        api_builder = "/weather?q="
        try:
            city = kwargs['city']
            country = kwargs['country']
        except:
            pass
        if not city:
            raise InvalidWeatherAPIRequestException
        api_builder += city.lower()
        if country:
            api_builder += "," + country.lower()
        # api_url + api_builder is the final url
