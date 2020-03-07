#!/usr/bin/python3
import socketserver

from http import server
from collections import namedtuple
from threading import Thread


PORT = 8181

callback = None
Client = namedtuple('Client', 'ip verb path')

def init(func):
	global callback
	callback = func
	httpd = socketserver.TCPServer(("127.0.0.1", PORT), GetHandler)
	return httpd

def run(httpd):	
	print('[*] WebServer Listening')
	httpd.serve_forever()
	
def close(httpd):

	def t_shutdown(httpd):
		httpd.shutdown()
		httpd.server_close()
		print('[*] WebServer Stopped')

	thread = Thread(target = t_shutdown, args = (httpd, ))
	thread.start()
	

class GetHandler(server.BaseHTTPRequestHandler):

	def do_GET(self):
		client = Client(\
			self.headers.get('X-Real-IP'),\
			"GET",\
			self.path\
			)
		callback(client)

	def do_POST(self):
		client = Client(\
			self.headers.get('X-Real-IP'),\
			"POST",\
			self.path\
			)
		
		callback(client)