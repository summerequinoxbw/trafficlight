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

#multiple MQTT brokers supported
clients = []
#optional indicator topic
indicatortopic = None

#this function is pretty useless, prints out a generic message everytime this script publishes to a topic
def on_publish(client,userdata,result):
	print('data published %s'%result)

#for logging purposes only
def on_disconnect(client, userdata, rc):
	now = datetime.now().strftime("%Y-%b-%d, %H:%M:%S")

#for logging purposes only
def on_connect(client, userdata, flags, rc):
	print("Connection returned result: "+connack_string(rc))

#changes lights based on the bool 'green'. POWER4 = red light, POWER3 = greenlight
def changeLights( green ):
	if not green:
		clients[0].publish('cmnd/traffic/POWER4', payload='off', qos=1, retain=False)
		time.sleep(1)
		clients[0].publish('cmnd/traffic/POWER3', payload='on', qos=1, retain=False)
	else:
		clients[0].publish('cmnd/traffic/POWER3', payload='off', qos=1, retain=False)
		time.sleep(1)
		clients[0].publish('cmnd/traffic/POWER4', payload='on', qos=1, retain=False)

#mqtt listener for changing the lights
def on_message_statechange(client, userdata, message):
	messagepayload = message.payload.decode('utf-8')
	messagetopic = message.topic

	print( messagepayload )

	if 'ON' in messagepayload:
		changeLights( True )
	elif 'OFF' in messagepayload:
		changeLights( False )

# if an indicator topic is specified, this function will publish to the indicatortopic the current state of POWER4.
# If the indicatortopic is the command topic of another tasmota power outlet then it will toggle the outlet to match the state of POWER4.
def on_message_changeindicator(client, userdata, message):
	messagepayload = message.payload.decode('utf-8')

	if indicatortopic is not None:
		print("changing indicator")
		clients[0].publish(indicatortopic, payload=messagepayload, qos=1, retain=False)

# main setup
def main(**kwargs):

	print("Starting traffic light controller")

	global clients
	global indicatortopic

	#if indicatortopic exists, use it
	if 'indicatortopic' in kwargs:
		indicatortopic = kwargs['indicatortopic']
		print("Indicator topic is: %s"%indicatortopic)
	else:
		indicatortopic = None

	#setup MQTT listeners
	clients.append(mqtt.Client())
	clients[0].on_publish = on_publish
	clients[0].on_connect = on_connect
	clients[0].on_disconnect = on_disconnect
	clients[0].connect(kwargs['mqtt-ip'], int(kwargs['mqtt-port']))
	clients[0].subscribe('stat/traffic/#')

	#TODO: make this a variable
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
