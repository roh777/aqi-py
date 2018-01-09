import requests
import sys
import urllib.parse

#get user location

def get_location():
	status_code = None
	try:
		loc_req = requests.get('http://ipinfo.io/json')
		status_code = loc_req.status_code
		if status_code is 200:
			loc_res = loc_req.json()
			city = loc_res['city']
			country = loc_res['country']
			coordinates = loc_res['loc'].split(',')
			print('You city determined by IP Address => {0}'.format(city))
			return {'city' : city}
		else:
			print("ERROR {0}: location search failed. Check you network ".format(status_code))
			return
	except Exception:
		print("ERROR {0}: location search failed. Check you network ".format(status_code))

		
def get_aqi_by_city(city):
	params = {'keyword' : city, 'token' : 'aa2aa1c21d4286431713a940b5e18aeb5f6fb3c0'}
	req_url = 'https://api.waqi.info/search/?'+urllib.parse.urlencode(params)
	#print (req_url)
	try:
		aqi_req = requests.get(req_url)
		if aqi_req.status_code == 200:
			aqi_res = aqi_req.json()
			station_list = aqi_res.get('data')
			if len(station_list) is 0:
				print('For location {}  no data available'.format(city))
				return False

			for station in station_list:
				print(station['station']['name'], station.get('aqi'))
			return True
		else:
			print('Error {0} Network error'.format(aqi_req.status_code))
	except Exception:
		print('Network failed which fetching AQI city data')


def get_aqi():
	city = get_location()
	if city is not None:
		get_aqi_by_city(city['city'])

def main():
	if len(sys.argv) > 1: 		#if user has provided city
		city = sys.argv[1]			
		if get_aqi_by_city(city) == False:
			print("Use command python aqi.py <City Name> or python aqi.py for location detection via IP address")
	else:					# if user has not provided
		get_aqi()

if __name__ == '__main__':
	main()
