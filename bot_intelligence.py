#!/usr/bin/python3
import requests
import shodan
import re
import json

from collections import namedtuple
#import abuseipdb

SHODAN_API_KEY = ""
ABUSEIPD_API_KEY = ""

ABUSE_IP_CHECK="https://www.abuseipdb.com/check/{}/json?key="+ABUSEIPD_API_KEY+"&days={}"

IP_API="http://ip-api.com/json/{}"

api = shodan.Shodan(SHODAN_API_KEY)


ShodanIntel = namedtuple('ShodanIntel', 'isp country_name tags')
MyipIntel = namedtuple('MyipIntel', 'isp country city')

def get_intel_shodan(ip):

	try:
		result = api.host(ip)
		intel = ShodanIntel(\
		result['data'][0]['isp'],\
		result['data'][0]['location']['country_name'],\
		result['data'][0]['tags'] if 'tags' in result['data'][0] else None\
		)
		return intel

	except:
		#print('Error: {}'.format(e))
		intel = ShodanIntel(\
		"No info",\
		"No info",\
		"No info"\
		)
		return intel

def get_intel_ipapi(ip):


	req = requests.get(IP_API.format(ip)).text
	data = json.loads(req)

	myipIntel = MyipIntel(\
	data['isp'],\
	data['country'],\
	data['city']\
	)
	return myipIntel

'''
def get_info_abuseipdb(ip):

	abuseipdb.configure_api_key(ABUSEIPD_API_KEY)
	info = abuseip.check_ip(ip=ip)
	return info
'''
