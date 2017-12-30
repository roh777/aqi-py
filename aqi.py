import requests
import urllib.parse

#get user location

def get_location():
	status_code = None
	try:
		loc_req = requests.get('http://ipinfo.io/json')
		status_code = loc_req.status_code
		if status_code is 200:
			loc_res = loc_req.json()
			city = loc_res['region']
			country = loc_res['country']
			coordinates = loc_res['loc'].split(',')
			return {'city' : city}
		else:
			print("ERROR {0}: location search failed. Check you network ".format(status_code))
			return
	except Exception:
		print("ERROR {0}: location search failed. Check you network ".format(status_code))

		
def get_aqi_by_city(city):
	print(city)
	params = {'keyword' : city, 'token' : 'aa2aa1c21d4286431713a940b5e18aeb5f6fb3c0'}
	req_url = 'https://api.waqi.info/search/?'+urllib.parse.urlencode(params)
	print (req_url)
	# try:
	aqi_req = requests.get(req_url)
	if aqi_req.status_code == 200:
		aqi_res = aqi_req.json()
		print(aqi_res)
	else:
		print('Error {0} Network error').format(aqi_req.status_code)
	# except Exception:
	# 	print('Network failed which fetching AQI city data')


def get_aqi():
	city = get_location()
	if city is not None:
		get_aqi_by_city(city['city'])

get_aqi()