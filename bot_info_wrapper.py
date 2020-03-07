#!/usr/bin/python3

def get_info(client, intelipapi, intelshodan):

	msg  = "IP: "+client.ip +\
	"\nVerb: "+ client.verb+\
	"\nPath: "+ client.path+\
	"\nIps: "+ intelipapi.isp+\
	"\nCountry: "+ intelipapi.country+\
	"\nCity: "+ intelipapi.city+\
	"\n\nLink: \n https://www.shodan.io/host/"+client.ip 
	
	return  msg