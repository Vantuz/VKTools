import requests
import time

class VKAPIHelper(object):
	def __init__(self, token = None):
		self.token = token;
		
	def apiRequest(self, method, params = {}):
		req_params = params
		if self.token != None:
			req_params['access_token'] = self.token
		req_params['v'] = "5.62"
		res = requests.get("https://api.vk.com/method/" + method, params=req_params).json()
		while 'error' in res and res['error']['error_code'] == 6:
			time.sleep(0.5)
			res = requests.get("https://api.vk.com/method/" + method, params=req_params).json()
		return res