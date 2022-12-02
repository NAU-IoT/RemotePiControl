#! /usr/bin/python

import paho.mqtt.client as mqtt
import lgpio
from pythonping import ping
from datetime import datetime
import pytz
import time
import RPRConfiguration as config

#import variables from config file
ResetPin = config.resetpin #establishes reset pin
Topic = config.topic    #establishes topic
SystemUnderTest = config.client #establishes system under test
Broker = config.broker #establishes broker
CA_Certs = config.cacert 
Certfile = config.certfile
Keyfile = config.keyfile
Timezone = config.timezone

h = lgpio.gpiochip_open(0)      #enable gpio
lgpio.gpio_claim_output(h, ResetPin) #set reset pin as output


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker
    client.subscribe(Topic)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
#    print(f"{msg.topic} {msg.payload}")
    if msg.payload.decode() == "reset":
        ts = datetime.now(pytz.timezone(Timezone))
        print(" ")
        print("Reset executed at: ",ts) #print time stamp when reset occurs
        print(" ")
        lgpio.gpio_write(h, ResetPin, 1) #set reset pin high
        string1 = "{} is being reset".format(SystemUnderTest) #formats string with hostname
        print(string1) #prints string 1 with hostname
        time.sleep(5) #wait 5 seconds
        lgpio.gpio_write(h, ResetPin, 0) #set reset pin low
        string2 = "{} has been reset".format(SystemUnderTest) #formats string with hostname
        print(string2)
        ping(SystemUnderTest, verbose=True, count = 12, interval = 3)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is turned off
client.will_set(Topic, b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
#client.tls_set(ca_certs=CA_Certs,
#               certfile=Certfile,
#               keyfile=Keyfile)

# create connection
client.connect(Broker, 1883, 60) #if using TLS, Broker is the common name on the server cert

#loop code
client.loop_forever()
