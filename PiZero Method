# This is the code that is to be ran on a RaspberryPiZero
# Code:

#! /usr/bin/python  #this makes the script executable in the command line with ./

import paho.mqtt.client as mqtt     #import paho module
import RPi.GPIO as io               #import GPIO module
import time

io.setmode(io.BCM)          #set board type for GPIO module
io.setwarnings(False)       #turn off warnings
io.cleanup()                #erase any previous instances of GPIO module
ResetPin = 22               #set ResetPin as 22
io.setup(ResetPin, io.OUT)  #set pin IO 22 as output (not actually pin 22, IO22, which is pin 15 on PiZero)

# define on_connect function
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continu>
    client.subscribe("RemotePiReset")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    if msg.payload.decode() == "reset":     #execute the Pi reset if reset is published to topic
        io.output(ResetPin, True)
        time.sleep(5)
        io.output(ResetPin, False)
        print("RaspberryPi has been reset")


#create client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is>
client.will_set('RemotePiReset', b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
client.tls_set(ca_certs="/home/pi/RemotePiReset/ca.crt",
               certfile="/home/pi/RemotePiReset/RemotePiReset.crt",
               keyfile="/home/pi/RemotePiReset/RemotePiReset.key")


# create connection, the three parameters are broker address, broker port numbe>
client.connect("test.mosquitto.org", 8883, 60)

# set the network loop blocking, it will not actively end the program before ca>
client.loop_forever()
