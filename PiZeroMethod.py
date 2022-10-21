#! /usr/bin/python

import paho.mqtt.client as mqtt
import RPi.GPIO as io
import time

#define the topic
topic = "[YOUR TOPIC HERE]"

io.setmode(io.BCM)
io.setwarnings(False)
io.cleanup()
ResetPin = 22   #IO pin 22 not actually pin 22 (actually pin 15 on PiZero)
io.setup(ResetPin, io.OUT)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe to the specified topic
    client.subscribe(topic)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    if msg.payload.decode() == "reset":
        io.output(ResetPin, True)
        print("RaspberryPi is being reset")
        time.sleep(5)
        io.output(ResetPin, False)
        print("RaspberryPi has been reset")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted
client.will_set(topic, b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
client.tls_set(ca_certs="/SOME/PATH/TO/ca.crt", #change path and central authority cert as necessary
               certfile="/SOME/PATH/TO/server.crt", #change path and certfile as necessary
               keyfile="/SOME/PATH/TO/server.key") #change path and keyfile as necessary

# create connection, the three parameters are broker address, broker port number, keepalive (only broker address and broker port number are required)
client.connect("[YOUR BROKER IP]", 8883, 60)

# set the network loop blocking, it will not actively end the program before ca>
client.loop_forever()
