#! /usr/bin/python

import logging
import paho.mqtt.client as mqtt
import lgpio
from pythonping import ping
from datetime import datetime
import pytz
import time
import yaml


def load_config():
   # Globalize config variable so relay states can be updated throughout script
   global config
   
   # Load the YAML file
   with open('/RPCConfiguration.yaml', 'r') as file:
       config = yaml.safe_load(file)
   # Globalize variables
   global Topic
   global Port
   global Broker
   global Load1
   global Load2
   global Load3
   global SystemUnderTest1
   global SystemUnderTest2
   global SystemUnderTest3
   global CA_Certs
   global Certfile
   global Keyfile
   global Timezone
   global Relay1State
   global Relay2State
   global Relay3State
   
   # Import variables from config file
   Topic = config['topic']
   Port = config['port']
   Broker = config['broker']
   Load1 = config['load1']
   Load2 = config['load2']
   Load3 = config['load3']
   SystemUnderTest1 = config['client1']	#establishes system under test 1
   SystemUnderTest2 = config['client2']	#establishes system under test 2
   SystemUnderTest3 = config['client3']	#establishes system under test 3
   CA_Certs = config['cacert']
   Certfile = config['certfile']
   Keyfile = config['keyfile']
   Timezone = config['timezone']
   Relay1State = config['Relay1State']
   Relay2State = config['Relay2State']
   Relay3State = config['Relay3State']


# Function to set relays to the value in the configuration file, 1 or 0 
def initialize_relays():
   lgpio.gpio_write(h, Relay1Pin, Relay1State) #set Relay1Pin to config file state
   lgpio.gpio_write(h, Relay2Pin, Relay2State) #set Relay2Pin to config file state
   lgpio.gpio_write(h, Relay3Pin, Relay3State) #set Relay1Pin to config file state

   
# Function to ping System Under Test to see if it is responding
def verify_ping(SystemUnderTest, Count):
    try:
       result = ping(SystemUnderTest, verbose=False, count = Count, interval = 2)
       if result.success():
          # The machine responds the ICMP request
          logging.debug("{} ICMP_REPLIED".format(SystemUnderTest))
          return True
       else:
          # The machine does NOT respond the ICMP request
          logging.debug("{} ICMP_IGNORED".format(SystemUnderTest))
          return False
    except Exception as e:
          logging.error(f"An error occurred while attempting to ping {SystemUnderTest}: {str(e)}")
          return None


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
def execute_stop(SystemUnderTest, Timezone, RelayPin, RelayState):
    ts = datetime.now(pytz.timezone(Timezone))
    tsString = str(ts)
    string0 = "\nStop executed at: {}\n".format(tsString) #formats string with timestamp
    logging.debug(string0) #print time stamp when stop occurs
    lgpio.gpio_write(h, RelayPin, 1) #set RelayPin pin high
    # Update the RelayState variable in config file
    config[str(RelayState)] = 1
    # Save the updated configuration back to the file
    with open('/RPCConfiguration.yaml', 'w') as file:
       yaml.dump(config, file)
    string1 = "{} has been stopped".format(SystemUnderTest) #formats string with hostname
    logging.debug(string1) #prints string 1 with hostname
    logging.debug("Verifying stop was executed...")
    time.sleep(3) #wait 3 seconds before pinging to make sure load is completely off
    try:
        verify_ping(SystemUnderTest, 5) # Parameters are (SystemUnderTest, Count)
    except socket.error:
        # No DNS resolution for host
        logging.debug("{} DNS_NO_RESOLUTION".format(SystemUnderTest))
    logging.debug("-"*100)


# Function to start the System Under Test
def execute_start(SystemUnderTest, Timezone, RelayPin, RelayState):
    ts = datetime.now(pytz.timezone(Timezone))
    tsString = str(ts)
    string0 = "\nStart executed at: {}\n".format(tsString) #formats string with timestamp
    logging.debug(string0) #print time stamp when start occurs
    lgpio.gpio_write(h, RelayPin, 0) #set Relay1Pin low
    # Update the RelayState variable in config file
    config[str(RelayState)] = 0
    # Save the updated configuration back to the file
    with open('/RPCConfiguration.yaml', 'w') as file:
       yaml.dump(config, file)
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
      result = verify_ping(SystemUnderTest, 5) # Parameters are (SystemUnderTest, Count)
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
    logging.debug(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    client.subscribe(Topic)


# The callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
  if(Load1):
    if msg.payload.decode() == "resetIOB":
       execute_reset(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if msg.payload.decode() == "stopIOB":
       execute_stop(SystemUnderTest1, Timezone, Relay1Pin, Relay1State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if msg.payload.decode() == "startIOB":
       execute_start(SystemUnderTest1, Timezone, Relay1Pin, Relay1State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if msg.payload.decode() == "statusIOB":
       execute_status(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
  if(Load2):
    if msg.payload.decode() == "resetNANO":
       execute_reset(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if msg.payload.decode() == "stopNANO":
       execute_stop(SystemUnderTest2, Timezone, Relay2Pin, Relay2State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if msg.payload.decode() == "startNANO":
       execute_start(SystemUnderTest2, Timezone, Relay2Pin, Relay2State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if msg.payload.decode() == "statusNANO":
       execute_status(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
  if(Load3):
    if msg.payload.decode() == "resetOPT":
       execute_reset(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if msg.payload.decode() == "stopOPT":
       execute_stop(SystemUnderTest3, Timezone, Relay3Pin, Relay3State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if msg.payload.decode() == "startOPT":
       execute_start(SystemUnderTest3, Timezone, Relay3Pin, Relay3State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if msg.payload.decode() == "statusOPT":
       execute_status(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
  if msg.payload.decode() == "resetall":
    if(Load1):
       execute_reset(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if(Load2):
       execute_reset(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if(Load3):
       execute_reset(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
  if msg.payload.decode() == "stopall":
    if(Load1):
       execute_stop(SystemUnderTest1, Timezone, Relay1Pin, Relay1State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if(Load2):
       execute_stop(SystemUnderTest2, Timezone, Relay2Pin, Relay2State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if(Load3):
       execute_stop(SystemUnderTest3, Timezone, Relay3Pin, Relay3State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
  if msg.payload.decode() == "startall":
    if(Load1):
       execute_start(SystemUnderTest1, Timezone, Relay1Pin, Relay1State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if(Load2):
       execute_start(SystemUnderTest2, Timezone, Relay2Pin, Relay2State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
    if(Load3):
       execute_start(SystemUnderTest3, Timezone, Relay3Pin, Relay3State) # Parameters are (SystemUnderTest, Timezone, RelayPin, RelayState)
  if msg.payload.decode() == "statusall":
    if(Load1):
       execute_status(SystemUnderTest1, Timezone, Relay1Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if(Load2):
       execute_status(SystemUnderTest2, Timezone, Relay2Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)
    if(Load3):
       execute_status(SystemUnderTest3, Timezone, Relay3Pin) # Parameters are (SystemUnderTest, Timezone, RelayPin)


def main():
    #enable logging
    logging.basicConfig(level=logging.DEBUG)
   
    # Load configuration
    load_config()

    # Globalize variables
    global Relay1Pin
    global Relay2Pin
    global Relay3Pin
    global h
   
    Relay1Pin = 26  #initialize Relay1Pin to GPIO 26, which is actually pin 37, if using standalone relay, hook jumper up to this pin
    Relay2Pin = 20  #initialize Relay2Pin to GPIO 20, which is actually pin 38, if using standalone relay, hook jumper up to this pin
    Relay3Pin = 21  #initialize Relay3Pin to GPIO 21, which is actually pin 40, if using standalone relay, hook jumper up to this pin
    
    h = lgpio.gpiochip_open(0)      #enable gpio
    lgpio.gpio_claim_output(h, Relay1Pin) #set Relay1Pin as output
    lgpio.gpio_claim_output(h, Relay2Pin) #set Relay2Pin as output
    lgpio.gpio_claim_output(h, Relay3Pin) #set Relay3Pin as output

    # Initialize relays to state in config file
    initialize_relays()
    
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


if __name__ == "__main__":
    main()
