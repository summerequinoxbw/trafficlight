# trafficlight

This project is based around a [generic smart powerbar](https://www.amazon.ca/dp/B076VRH9WP) running [Tasmota 
firmware](https://tasmota.github.io/docs/). The purpose of this script/docker container is to receive input 
(from the web, mqtt broker, other tasmota devices, etc) and toggle the state of outlet 3 and 4 (while ensuring 
that they maintain the opposite state at all times). In addition to this it can optionally activate another 
tasmota/generic MQTT listening device based on the state of outlet 4.


