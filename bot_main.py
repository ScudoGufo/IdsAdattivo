#!/usr/bin/python3
import bot_server
import bot_telegram
import bot_database
import bot_intelligence

from signal import signal, SIGINT
from sys import exit

def callback(client):
	intelipapi = bot_intelligence.get_intel_ipapi(client.ip)
	intelshodan = bot_intelligence.get_intel_shodan(client.ip)
	bot_database.insert_request(db, cursor, client, intelipapi, intelshodan)
	bot_telegram.send_alert(client, intelipapi, intelshodan, telegram)


def quit(signal_received, frame):
	# Handle any cleanup here
	print('\n[*] Quitting')
	bot_database.close(db, cursor)
	bot_telegram.close(updater)
	bot_server.close(httpd)

	exit(0)

if __name__ == '__main__':
	signal(SIGINT, quit)
	print('[*] Starting')

	db, cursor = bot_database.init()
	updater, telegram = bot_telegram.init(cursor)
	httpd = bot_server.init(callback)
	bot_server.run(httpd)