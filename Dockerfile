FROM alpine

LABEL maintainer="David Rickett"


ENV TZ=Etc/UTC
ENV MQTT_IP=mqtt-broker
ENV MQTT_PORT=1883
ENV INDICATORTOPIC=''

RUN apk add --no-cache \
	python3 \
	tzdata \ 
	py3-pip

RUN pip3 install paho-mqtt

COPY ./trafficlight-controller.py /usr/share/trafficlight-controller.py
RUN chmod +x /usr/share/trafficlight-controller.py

ENTRYPOINT python3 -u /usr/share/trafficlight-controller.py mqtt-ip=$MQTT_IP mqtt-port=$MQTT_PORT indicatortopic=$INDICATORTOPIC

