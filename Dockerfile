# syntax=docker/dockerfile:1

FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y python3-smbus python3-dev i2c-tools

RUN apt-get install -y software-properties-common

RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa

RUN apt-get -y install cron

RUN apt-get install -y mosquitto mosquitto-clients

COPY mosquitto.conf /etc/mosquitto/

RUN pip3 install paho-mqtt

RUN pip3 install rpi.gpio

RUN apt install -y python3-lgpio

RUN pip install pytz

RUN pip install pythonping

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

ENV TZ=America/Phoenix

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /Data

RUN mkdir -p /Data/logs

ADD RPCConfiguration.py /RPCConfiguration.py

ADD RemotePiControl.py /RemotePiControl.py

ADD RemotePiControl.sh /RemotePiControl.sh

ADD crontab /etc/cron.d/simple-cron

RUN touch /var/log/cron.log

RUN chmod 0644 /etc/cron.d/simple-cron

RUN chmod +x /RemotePiControl.py

RUN chmod +x /RemotePiControl.sh

# sleep command to give mosquitto time to start before using.
CMD service mosquitto start \
    && sleep 5 \
    && cron \
#Uncomment the line below and comment out the above line for debugging, otherwise script will not execute until midnight
#    && ./RemotePiControl.sh \ 
    && bash
