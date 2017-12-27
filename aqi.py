import requests

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
			print(city, country, coordinates)
		else:
			print("ERROR {0}: location search failed. Check you network ".format(status_code))
	except Exception:
		print("ERROR {0}: location search failed. Check you network ".format(status_code))

get_location()

# make request to  AQI CN for city