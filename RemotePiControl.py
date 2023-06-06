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
lgpio.gpio_claim_output(h, Relay2Pin) #set Relay2Pin as output
lgpio.gpio_claim_output(h, Relay3Pin) #set Relay3Pin as output


# Function to ping System Under Test to see if it is responding
def verify_ping(SystemUnderTest, Count):
    result = ping(SystemUnderTest, verbose=False, count = Count, interval = 2)
    if result.success():
       # The machine responds the ICMP request
       logging.debug("{} ICMP_REPLIED".format(SystemUnderTest))
       return True
    else:
       # The machine does NOT respond the ICMP request
       logging.debug("{} ICMP_IGNORED".format(SystemUnderTest))
       return False


# Function to reset the System Under Test    
def execute_reset(SystemUnderTest, Timezone, RelayPin):
    ts = datetime.now(pytz.timezone(Timezone))
    tsString = str(ts)
    string0 = "\nReset executed at: {}\n".format(tsString) #formats string with timestamp
    logging.debug(string0) #print time stamp when reset occurs
    lgpio.gpio_write(h, RelayPin, 1) #set Relay1Pin high
    string1 = "{} is being reset".format(SystemUnderTest) #formats string with hostname
    logging.debug(string1) #prints string 1 with hostname
    time.sleep(5) #wait 5 seconds
    lgpio.gpio_write(h, RelayPin, 0) #set Relay1Pin low
    string2 = "{} has been reset".format(SystemUnderTest) #formats string with hostname
    logging.debug(string2)
    logging.debug("Please wait while the reset is confirmed...")
    try:
        verify_ping(SystemUnderTest, 20) # Parameters are (SystemUnderTest, Count)
    except socket.error:
        # No DNS resolution for host  
        logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest))
    logging.debug("-"*100)
  

# Function to stop the System Under Test       
def execute_stop(SystemUnderTest, Timezone, RelayPin):
    ts = datetime.now(pytz.timezone(Timezone))
    tsString = str(ts)
    string0 = "\nStop executed at: {}\n".format(tsString) #formats string with timestamp
    logging.debug(string0) #print time stamp when stop occurs
    lgpio.gpio_write(h, RelayPin, 1) #set Relay1Pin pin high
    string1 = "{} has been stopped".format(SystemUnderTest) #formats string with hostname
    logging.debug(string1) #prints string 1 with hostname
    logging.debug("Verifying stop was executed...")
    time.sleep(3) #wait 3 seconds before pinging to make sure load is completely off
    try:
        verify_ping(SystemUnderTest, 5) # Parameters are (SystemUnderTest, Count)
    except socket.error:
        # No DNS resolution for host 
        logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest)
    logging.debug("-"*100)

                       
# Function to start the System Under Test                      
def execute_start(SystemUnderTest, Timezone, RelayPin):
    ts = datetime.now(pytz.timezone(Timezone))
    tsString = str(ts)
    string0 = "\nStart executed at: {}\n".format(tsString) #formats string with timestamp
    logging.debug(string0) #print time stamp when start occurs  
    lgpio.gpio_write(h, RelayPin, 0) #set Relay1Pin low
    string1 = "{} has been started".format(SystemUnderTest) #formats string with hostname
    logging.debug(string1) #prints string 1 with hostname
    logging.debug("Verifying start was executed...")
    try:
      verify_ping(SystemUnderTest, 20) # Parameters are (SystemUnderTest, Count)
    except socket.error:
      # No DNS resolution for host 
      logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest))
    logging.debug("-"*100)                    

                       
# Function to get the current status of the System Undert Test
def execute_status(SystemUnderTest, Timezone, RelayPin):
    ts = datetime.now(pytz.timezone(Timezone))
    tsString = str(ts)
    string0 = "\nStatus executed at: {}\n".format(tsString) #formats string with timestamp
    logging.debug(string0) #print time stamp when reset occurs
    logging.debug("Checking status...")
    try:
      result = verify_ping(SystemUnderTest, 20) # Parameters are (SystemUnderTest, Count)
      if(result == True):
         # System is online and responding
         logging.debug("STATUS: ON")
      else:
         # System is offline
         logging.debug("STATUS: OFF")
    except socket.error:
      # No DNS resolution for host
      logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest))
    logging.debug("-"*100)


# define on_connect function
def on_connect(client, userdata, flags, rc):
    # logging.debug(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    client.subscribe(Topic)

                       
# The callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
  if(Load1):
    if msg.payload.decode() == "reset1":
       execute_reset(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

    if msg.payload.decode() == "stop1":
       execute_stop(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

    if msg.payload.decode() == "start1":
       execute_start(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
        
    if msg.payload.decode() == "status1":
       execute_status(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
         
  if(Load2):    
    if msg.payload.decode() == "reset1":
       execute_reset(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

    if msg.payload.decode() == "stop1":
       execute_stop(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

    if msg.payload.decode() == "start1":
       execute_start(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

        
    if msg.payload.decode() == "status1":
       execute_status(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
  
  if(Load3):      
    if msg.payload.decode() == "reset3":
       execute_reset(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

    if msg.payload.decode() == "stop3":
       execute_stop(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

    if msg.payload.decode() == "start3":
       execute_start(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
        
    if msg.payload.decode() == "status3":
       execute_status(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)

#create client instance
client = mqtt.Client()                       

# Set callback functions for client
client.on_connect = on_connect
client.on_message = on_message

# Set the will message, when the client unexpedetly disconnects or terminates its connection, this will publish
client.will_set(Topic, b'{"status": "Off"}')

#establish tls set for secure connection over port 8883
#client.tls_set(ca_certs=CA_Certs,
#               certfile=Certfile,
#               keyfile=Keyfile)

# Create connection, the three parameters are broker address, broker port number, and keep alive time
client.connect(Broker, Port, 60) #If using TLS, Broker is the common name on the server cert

# set the network loop blocking, maintains the network connection and prevents program execution
client.loop_forever()
