#!/usr/bin/env python

__author__ = "David Rickett"
__credits__ = ["David Rickett"]
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "David Rickett"
__email__ = "dap.rickett@gmail.com"
__status__ = "Production"

import serial
import os
import re
import sys
import random
import time
import paho.mqtt.client as mqtt
from datetime import datetime

#serial messages "object,number,[open/closed]"

#ser = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Micro-if00')  # open serial port
ser = 0

def setupSerial(vid, pid):
	global ser
	now = datetime.now().strftime("%Y-%b-%d, %H:%M:%S")
	print('%s: Initializing serial for %s:%s'%(now, vid, pid))
	ser = serial.serial_for_url('hwgrep://%s:%s'%(vid, pid))

def on_publish(client,userdata,result):
#	print(f'data published {result}\n')
	pass

def on_disconnect(client, userdata, rc):
	now = datetime.now().strftime("%Y-%b-%d, %H:%M:%S")
	print('%s: Disconnected'%now)

def on_connect(client, userdata, flags, rc):
	print("Connection returned result: "+connack_string(rc))

def main(**kwargs):
	global ser
	setupSerial(kwargs['vid'],kwargs['pid'])
	clients = []
	clients.append(mqtt.Client())
	clients[0].on_publish = on_publish
	clients[0].on_connect = on_connect
	clients[0].on_disconnect = on_disconnect
	clients[0].connect(kwargs['mqtt-ip'], int(kwargs['mqtt-port']),keepalive=60)
	clients[0].loop_start()
	if( 'mqtt-ip-alt' in kwargs ):
		if( kwargs['mqtt-ip'] != kwargs['mqtt-ip-alt'] ):
			clients.append(mqtt.Client())
			clients[1].on_publish = on_publish
			clients[1].on_connect = on_connect
			clients[1].on_disconnect = on_disconnect
			clients[1].connect(kwargs['mqtt-ip-alt'], int(kwargs['mqtt-port-alt']),keepalive=60)
			clients[1].loop_start()

	#TODO: Refactor this whole thing
	while( True ):
		line = ser.readline().decode("utf-8").strip()
		now = datetime.now().strftime("%Y-%b-%d, %H:%M:%S")
		print( '%s: %s'%(now, line) )

# stat/trafficcontrol/button0 ON = red
# stat/trafficcontrol/button2 ON = green

		#green light
		if 'button2' in line:
			for client in clients:
				result = client.publish('cmnd/traffic/POWER3',payload='ON')
				print(result)
		#red light
		elif 'button0' in line:
			for client in clients:
				result = client.publish('cmnd/traffic/POWER4',payload='ON')
				print(result)
		else:
			for client in clients:
				result = client.publish(line.split(' ')[0],'ON')
				print(result)


if __name__== "__main__":
	main(**dict(arg.split('=') for arg in sys.argv[1:]))
