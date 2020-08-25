# trafficlight

![Image of my handywork](/img/trafficlight.jpg)

This project is based around a [generic smart powerbar](https://www.amazon.ca/dp/B076VRH9WP) running [Tasmota 
firmware](https://tasmota.github.io/docs/). The purpose of this script/docker container is to receive input 
(from the web, mqtt broker, other tasmota devices, etc) and toggle the state of outlet 3 and 4 (while ensuring 
that they maintain the opposite state at all times). In addition to this it can optionally activate another 
tasmota/generic MQTT listening device based on the state of outlet 4.

# Setup

Currently there are four discrete devices in the setup:

* An MQTT relay, I use the [dockerized Eclipse Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) package.
* The Traffic Light, a [generic smart powerbar](https://www.amazon.ca/dp/B076VRH9WP) running [Tasmota
firmware](https://tasmota.github.io/docs/) with two lamp extension cords plugged in. One plug ("POWER3") has a green party bulb, the other ("POWER4") has a red party bulb.
* The control box, which consists of a bank of buttons (minimum two), an arduino and a device (in this case a Raspberry Pi 1 B) to take serial messages from the arduino and punt them over the network.
* An indicator light (optional), with the way the traffic light is built there is no way to see the states from the cashier's position, this is just another smart plug running the same opensource firmware previously mentioned.

For the traffic (and indicator) light itself, install tasmota and follow the first time setup on the tasmota project's website, for reference the template for the smart plug used in this project can be found [on blakadder.com](https://templates.blakadder.com/heyvalue_HLT-331.html). Note: It is quite handy to go into the smart power bar's console and set the outlets on the light bulbs to be `interlock` as detailed on [the tasmota wiki](https://tasmota.github.io/docs/Commands/), this makes some aspects of control simpler.

If an external indicator is needed: configure the environmental variables, pointing to your MQTT broker and the control topic of the indicator plug in docker-compose.traffic.yaml and then execute `docker-compose -f docker-compose.traffic.yaml up --build -d`. Currently commands are hardcoded to be sent in the `cmnd/traffic/#` topic, but I'm sure you can adapt that.

For the control box you will need to compile and flash an arduino with the .ino file and wire it to a set of buttons. Per code example I have wired 4 pairs of cat5e wiring across 4 buttons and the first four interrupt pins of an Arduino Micro (ATmega32U4). Install `trafficlightcontrol.py` to an easily accessible location and place `systemd-trafficlight.service` in `/etc/systemd/system/`.


