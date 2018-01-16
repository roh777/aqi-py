#!/usr/bin/env python

import requests
import sys
#for command line arguments
import argparse
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
	
	try:
		aqi_req = requests.get(req_url)
		if aqi_req.status_code == 200:
			aqi_res = aqi_req.json()
			station_list = aqi_res.get('data')
			if len(station_list) is 0:
				print('For location {}  no data available'.format(city))
				return False

			for station in station_list:
				print("{0}-[{1}] ({2})".format(station['station']['name'], station.get('aqi'), station['time']['stime']))
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
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--city", help="enter a city name for which you wold like to see AQI", type=str)
	args = parser.parse_args()

	if args.city: 		#if user has provided city
		get_aqi_by_city(args.city)
	else:					# if user has not provided
		get_aqi()

if __name__ == '__main__':
	main()
