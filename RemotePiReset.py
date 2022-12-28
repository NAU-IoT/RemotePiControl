#! /usr/bin/python

import logging
import paho.mqtt.client as mqtt
import lgpio
from pythonping import ping
from datetime import datetime
import pytz
import time
import RPRConfiguration as config

#enable logging
logging.basicConfig(level=logging.DEBUG)

#import variables from config file
ResetPin = config.resetpin #establishes reset pin
Topic = config.topic	#establishes topic
SystemUnderTest = config.client	#establishes system under test
Broker = config.broker #establishes broker
CA_Certs = config.cacert
Certfile = config.certfile
Keyfile = config.keyfile
Timezone = config.timezone

h = lgpio.gpiochip_open(0)	#enable gpio
lgpio.gpio_claim_output(h, ResetPin) #set reset pin as output

#create client instance
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continu>
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
    if msg.payload.decode() == "reset":
        ts = datetime.now(pytz.timezone(Timezone))
        tsString = str(ts)
        string0 = "\nReset executed at: {}\n".format(tsString) #formats string with timestamp
        logging.debug(string0) #print time stamp when reset occurs
        lgpio.gpio_write(h, ResetPin, 1) #set reset pin high
        string1 = "{} is being reset".format(SystemUnderTest) #formats string with hostname
        logging.debug(string1) #prints string 1 with hostname
        time.sleep(5) #wait 5 seconds
        lgpio.gpio_write(h, ResetPin, 0) #set reset pin low
        string2 = "{} has been reset".format(SystemUnderTest) #formats string with hostname
        logging.debug(string2)
        logging.debug("Please wait while the reset is confirmed...")
        try:
            result = ping(SystemUnderTest, verbose=False, count = 12, interval = 3)
            # the machine responds the ICMP request
            if result.success():
                 logging.debug("{} ICMP_REPLIED".format(SystemUnderTest))
            #the machine does NOT respond the ICMP request
            else:
                 logging.debug("{} ICMP_IGNORED".format(SystemUnderTest))
        # no DNS resolution for host
        except socket.error:
            #pass
            logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest))
        logging.debug("-"*100)

client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is>
client.will_set(Topic, b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
#client.tls_set(ca_certs=CA_Certs,
#               certfile=Certfile,
#               keyfile=Keyfile)

# create connection, the three parameters are broker address, broker port numbe>
client.connect(Broker, 1883, 60) #IP is the common name on the server cert

# set the network loop blocking, it will not actively end the program before ca>
client.loop_forever()
