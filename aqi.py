#!/usr/bin/env python

import requests
import sys
#for command line arguments
import argparse
import urllib.parse

#class with color codes for output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGNETA = '\033[35m'



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

			# for station in station_list:
			# 	print("{0}-[{1}] ({2})".format(station['station']['name'], station.get('aqi'), station['time']['stime']))
			return station_list
		else:
			print('Error {0} Network error'.format(aqi_req.status_code))
	except Exception:
		print('Network failed which fetching AQI city data')

def process_time_string(time_str):
	#process time string from 2018-01-16 03:00:00 to 16/1/18,3:00AM
	try:
		d,t = time_str.split(' ')
		rev_d= d.split('-')[::-1]
		date = '/'.join([rev_d[0] , rev_d[1] , rev_d[2][2:] ])
		h,m, s= t.split(':')
		suffix = None
		if 24 > int(h) > 12: 
			suffix = 'PM'
		else: 
			suffix = 'AM'

		time = h +':'+ m + suffix
		return time + ','+date
	except ValueError:
		return time_str

def process_aqi(aqi_str):
	try:
		aqi = int(aqi_str)
		if 0 <= aqi < 100:
			return bcolors.OKGREEN + bcolors.BOLD  + aqi_str + bcolors.ENDC
		if 100 <= aqi <= 200:
			return bcolors.WARNING + bcolors.BOLD  + aqi_str + bcolors.ENDC
		if aqi > 200:
			return bcolors.FAIL + bcolors.BOLD  + aqi_str + bcolors.ENDC

	except ValueError:
		return aqi_str



def print_aqi_data(stations): #gets aqi data (stations list) and prints them
	for st in stations:
		name = bcolors.BOLD + st['station']['name'] + bcolors.ENDC
		aqi_str = st.get('aqi')
		time_str = st['time']['stime']

		aqi = process_aqi(aqi_str)
		time = process_time_string(time_str)

		print('{0} [{1}]({2})'.format(name,aqi,time))


def get_aqi():
	city = get_location()
	if city is not None:
		get_aqi_by_city(city['city'])

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--city", help="enter a city name for which you wold like to see AQI", type=str)
	args = parser.parse_args()

	if args.city: 		#if user has provided city
		aqi_data = get_aqi_by_city(args.city)
		if aqi_data:
			print_aqi_data(aqi_data)
	else:					# if user has not provided
		get_aqi()

if __name__ == '__main__':
	main()
