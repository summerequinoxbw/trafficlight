# trafficlight

![Image of my handywork](/img/trafficlight.jpg)

This project is based around a [generic smart powerbar](https://www.amazon.ca/dp/B076VRH9WP) running [Tasmota 
firmware](https://tasmota.github.io/docs/). The purpose of this script/docker container is to receive input 
(from the web, mqtt broker, other tasmota devices, etc) and toggle the state of outlet 3 and 4 (while ensuring 
that they maintain the opposite state at all times). In addition to this it can optionally activate another 
tasmota/generic MQTT listening device based on the state of outlet 4.

#Setup

Currently there are four discrete devices in the setup:

* An MQTT relay, I use the [dockerized Eclipse Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) package.
* The Traffic Light, a [generic smart powerbar](https://www.amazon.ca/dp/B076VRH9WP) running [Tasmota
firmware](https://tasmota.github.io/docs/) with two lamp extension cords plugged in. One plug ("POWER3") has a green party bulb, the other ("POWER4") has a red party bulb.
* The control box, which consists of a bank of buttons (minimum two), an arduino and a device (in this case a Raspberry Pi 1 B) to take serial messages from the arduino and punt them over the network.
* An indicator light (optional), with the way the traffic light is built there is no way to see the states from the cashier's position, this is just another smart plug running the same opensource firmware previously mentioned.

