'''
API_Connection: Base api connection class that stores api url endpoint
'''
class APIConnection:
	def __init__(self, api_url):
		self.api_url = api_url
