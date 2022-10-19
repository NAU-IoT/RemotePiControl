# RemotePiReset
This repository contains code to be uploaded onto a D1 Mini Pro to facilitate a remote reset on a RaspberryPi. 

This solution can also be done using a RaspberryPiZero, which is also documented here.

This solution is intended to be ran as the root user.

## D1MiniPro Solution

### Components:

**D1MINI PRO**

   Used to interpret reset command over MQTT and send resetting signal to relay
    
**RASPBERRY PI**

   Wired through the relay, this is what is being reset
    
**5V RELAY**

   Wired so that when the D1Mini sends the reset signal, the relay cuts power to the Rpi for 5 seconds.
    
   
Steps:
- Copy source code into Arduino IDE (found in D1Code)
- Upload onto D1MiniPro
- Wire D1Mini to other components
- Publish reset command to topic from broker
- Done!
    
    
## RaspberryPIZero Solution

### Components:

**RaspberryPiZero**

   Used to interpret reset command over MQTT and send resetting signal to relay
    
**RASPBERRY PI**

   Wired through the relay, this is what is being reset
    
**5V RELAY**

   Wired so that when the PiZero sends the reset signal, the relay cuts power to the Rpi for 5 seconds.

The principal is the exact same as the D1Mini solution, but the D1Mini is subsituted with the RaspberryPiZero. If you want to run MQTT using python on a RaspberryPiZero these are the steps:

### Dependencies:

Install the paho.mqtt library:

`git clone https://github.com/eclipse/paho.mqtt.python`

`cd paho.mqtt.python`

`python3 setup.py install`

Install the GPIO package:

`apt-get install rpi.gpio`

After installing dependencies: 

- Create script using nano
- Write source code into new script (code can be found in PiZeroMethod)
- Save file as {YourFileName}.py
- Verify that permissions are set so that the script is executable by typing `chmod +x SCRIPTNAME.py` in the command line
- Use command `sudo su` to get root user permissions (script only works when ran with root permissions)
- Type `./{YourFileName}.py` into the command line to execute the script
- Publish reset command to topic from broker
- Done!




