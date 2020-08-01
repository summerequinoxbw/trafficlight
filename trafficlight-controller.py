#!/usr/bin/env python3

__author__ = "David Rickett"
__credits__ = ["David Rickett"]
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "David Rickett"
__email__ = "dap.rickett@gmail.com"
__status__ = "Production"

import os
import re
import sys
import time

import paho.mqtt.client as mqtt
from datetime import datetime

clients = []
indicatortopic = None

def on_publish(client,userdata,result):
	print('data published %s\n'%result)

def on_disconnect(client, userdata, rc):
	now = datetime.now().strftime("%Y-%b-%d, %H:%M:%S")

def on_connect(client, userdata, flags, rc):
	print("Connection returned result: "+connack_string(rc))

def changeLights( green ):
	if not green:
		clients[0].publish('cmnd/traffic/POWER4', payload='off', qos=1, retain=False)
		time.sleep(1)
		clients[0].publish('cmnd/traffic/POWER3', payload='on', qos=1, retain=False)
	else:
		clients[0].publish('cmnd/traffic/POWER3', payload='off', qos=1, retain=False)
		time.sleep(1)
		clients[0].publish('cmnd/traffic/POWER4', payload='on', qos=1, retain=False)

def on_message_statechange(client, userdata, message):
	messagepayload = message.payload.decode('utf-8')
	messagetopic = message.topic

	print( messagepayload )

	if 'ON' in messagepayload:
		changeLights( True )
	elif 'OFF' in messagepayload:
		changeLights( False )

def on_message_changeindicator(client, userdata, message):
	messagepayload = message.payload.decode('utf-8')

	if indicatortopic is not None:
		clients[0].publish(indicatortopic, payload=messagepayload, qos=1, retain=False)

def main(**kwargs):

	print("Starting traffic light controller")

	global clients

	if 'indicatortopic' in kwargs:
		indicatortopic = kwargs['indicatortopic']
	else:
		indicatortopic = None

	clients.append(mqtt.Client())
	clients[0].on_publish = on_publish
	clients[0].on_connect = on_connect
	clients[0].on_disconnect = on_disconnect
	clients[0].connect(kwargs['mqtt-ip'], int(kwargs['mqtt-port']))
	clients[0].subscribe('stat/traffic/#')
	clients[0].message_callback_add(
		'stat/traffic/POWER5',
		on_message_statechange)
	clients[0].message_callback_add(
		'stat/traffic/POWER4',
		on_message_changeindicator)
#	client.on_message=on_message
	clients[0].loop_start()

	while ( True ):
		time.sleep(30)

if __name__== "__main__":
	main(**dict(arg.split('=') for arg in sys.argv[1:]))
