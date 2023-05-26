#! /usr/bin/python

import logging
import paho.mqtt.client as mqtt
import lgpio
from pythonping import ping
from datetime import datetime
import pytz
import time
import RPCConfiguration as config

#enable logging
logging.basicConfig(level=logging.DEBUG)

#import variables from config file
Topic = config.topic	#establishes topic
Port = config.port
SystemUnderTest1 = config.client1	#establishes system under test 1
SystemUnderTest2 = config.client2	#establishes system under test 2
SystemUnderTest3 = config.client3	#establishes system under test 3
Broker = config.broker #establishes broker
CA_Certs = config.cacert
Certfile = config.certfile
Keyfile = config.keyfile
Timezone = config.timezone
Load1 = config.load1
Load2 = config.load2
Load3 = config.load3

Relay1Pin = 26  #initialize Relay1Pin to GPIO 26, which is actually pin 37, if using standalone relay, hook jumper up to this pin
Relay2Pin = 20  #initialize Relay2Pin to GPIO 20, which is actually pin 38, if using standalone relay, hook jumper up to this pin
Relay3Pin = 21  #initialize Relay3Pin to GPIO 21, which is actually pin 40, if using standalone relay, hook jumper up to this pin
h = lgpio.gpiochip_open(0)      #enable gpio
lgpio.gpio_claim_output(h, Relay1Pin) #set Relay1Pin as output

#create client instance
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    client.subscribe(Topic)

#define the publish function
def publish(self, topic, data, qos=1, retain=False):
    """
      Publish to a topic.
    """
    logging.info("Publishing to topic %s" % topic)
    self.client.publish(topic, data, qos=qos, retain=retain)


# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
#    print(f"{msg.topic} {msg.payload}")
  if(Load1):
    if msg.payload.decode() == "reset1":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nReset executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        lgpio.gpio_write(h, Relay1Pin, 1) #set Relay1Pin high
        string1 = "{} is being reset".format(SystemUnderTest1) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        time.sleep(5) #wait 5 seconds
        lgpio.gpio_write(h, Relay1Pin, 0) #set Relay1Pin low
        string2 = "{} has been reset".format(SystemUnderTest1) #formats string with hostname
        logging.debug(string2)
        logging.debug("Please wait while the reset is confirmed...")
        try:
            result = ping(SystemUnderTest1, verbose=False, count = 20, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest1))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest1))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest1))
        logging.debug("-"*100)

    if msg.payload.decode() == "stop1":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStop executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when stop occurs
        lgpio.gpio_write(h, Relay1Pin, 1) #set Relay1Pin pin high
        string1 = "{} has been stopped".format(SystemUnderTest1) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        logging.debug("Verifying stop was executed...")
        time.sleep(3) #wait 3 seconds before pinging to make sure load is completely off
        try:
            result = ping(SystemUnderTest1, verbose=False, count = 5, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest1))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest1))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest1))
        logging.debug("-"*100)

    if msg.payload.decode() == "start1":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStart executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when start occurs
        lgpio.gpio_write(h, Relay1Pin, 0) #set Relay1Pin low
        string1 = "{} has been started".format(SystemUnderTest1) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        logging.debug("Verifying start was executed...")
        try:
            result = ping(SystemUnderTest1, verbose=False, count = 20, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest1))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest1))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest1))
        logging.debug("-"*100)
        
    if msg.payload.decode() == "status1":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStatus executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        logging.debug("Checking status...")
        try:
            result = ping(SystemUnderTest1, verbose=False, count = 5, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest1))
                 logging.debug("STATUS: ON")
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest1))
                 logging.debug("STATUS: OFF")
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest1))
        logging.debug("-"*100)
        
        
    if(Load2):    
      if msg.payload.decode() == "reset2":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nReset executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        lgpio.gpio_write(h, Relay1Pin, 1) #set Relay1Pin high
        string1 = "{} is being reset".format(SystemUnderTest2) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        time.sleep(5) #wait 5 seconds
        lgpio.gpio_write(h, Relay1Pin, 0) #set Relay1Pin low
        string2 = "{} has been reset".format(SystemUnderTest2) #formats string with hostname
        logging.debug(string2)
        logging.debug("Please wait while the reset is confirmed...")
        try:
            result = ping(SystemUnderTest2, verbose=False, count = 20, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest2))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest2))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest2))
        logging.debug("-"*100)

    if msg.payload.decode() == "stop2":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStop executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when stop occurs
        lgpio.gpio_write(h, Relay1Pin, 1) #set Relay1Pin pin high
        string1 = "{} has been stopped".format(SystemUnderTest2) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        logging.debug("Verifying stop was executed...")
        time.sleep(3) #wait 3 seconds before pinging to make sure load is completely off
        try:
            result = ping(SystemUnderTest2, verbose=False, count = 5, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest2))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest2))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest2))
        logging.debug("-"*100)

    if msg.payload.decode() == "start2":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStart executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when start occurs
        lgpio.gpio_write(h, Relay1Pin, 0) #set Relay1Pin low
        string1 = "{} has been started".format(SystemUnderTest2) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        logging.debug("Verifying start was executed...")
        try:
            result = ping(SystemUnderTest2, verbose=False, count = 20, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest2))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest2))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest2))
        logging.debug("-"*100)
       
    if msg.payload.decode() == "status2":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStatus executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        logging.debug("Checking status...")
        try:
            result = ping(SystemUnderTest2, verbose=False, count = 5, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest2))
                 logging.debug("STATUS: ON")
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest2))
                 logging.debug("STATUS: OFF")
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest2))
        logging.debug("-"*100)

        
  if(Load3):      
    if msg.payload.decode() == "reset3":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nReset executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        lgpio.gpio_write(h, Relay1Pin, 1) #set Relay1Pin high
        string1 = "{} is being reset".format(SystemUnderTest3) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        time.sleep(5) #wait 5 seconds
        lgpio.gpio_write(h, Relay1Pin, 0) #set Relay1Pin low
        string2 = "{} has been reset".format(SystemUnderTest3) #formats string with hostname
        logging.debug(string2)
        logging.debug("Please wait while the reset is confirmed...")
        try:
            result = ping(SystemUnderTest3, verbose=False, count = 20, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest3))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest3))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest3))
        logging.debug("-"*100)

    if msg.payload.decode() == "stop3":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStop executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when stop occurs
        lgpio.gpio_write(h, Relay1Pin, 1) #set Relay1Pin pin high
        string1 = "{} has been stopped".format(SystemUnderTest3) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        logging.debug("Verifying stop was executed...")
        time.sleep(3) #wait 3 seconds before pinging to make sure load is completely off
        try:
            result = ping(SystemUnderTest3, verbose=False, count = 5, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest3))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest3))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest3))
        logging.debug("-"*100)

    if msg.payload.decode() == "start3":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStart executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when start occurs
        lgpio.gpio_write(h, Relay1Pin, 0) #set Relay1Pin low
        string1 = "{} has been started".format(SystemUnderTest3) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        logging.debug("Verifying start was executed...")
        try:
            result = ping(SystemUnderTest3, verbose=False, count = 20, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest3))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest3))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest3))
        logging.debug("-"*100)
        
    if msg.payload.decode() == "status3":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nStatus executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        logging.debug("Checking status...")
        try:
            result = ping(SystemUnderTest3, verbose=False, count = 5, interval = 2)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest3))
                 logging.debug("STATUS: ON")
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest3))
                 logging.debug("STATUS: OFF")
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest3))
        logging.debug("-"*100)

        
        
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted
client.will_set(Topic, b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
#client.tls_set(ca_certs=CA_Certs,
#               certfile=Certfile,
#               keyfile=Keyfile)

# create connection, the three parameters are broker address, broker port numbe>
client.connect(Broker, Port, 60) #IP is the common name on the server cert

# set the network loop blocking, it will not actively end the program before ca>
client.loop_forever()
