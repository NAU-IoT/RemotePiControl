# RemotePiReset
This repository contains code to be uploaded onto a D1 Mini Pro to facilitate a remote reset on a RaspberryPi. 

This solution can also be done using a RaspberryPiZero, which is also documented here.


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

**Raspberry Pi 4**

   Used to interpret reset command over MQTT and send resetting signal to relay
    
**RASPBERRY PI IO Board**

   Wired through the relay, this is what is being reset
    
**5V RELAY**

   Wired so that when the Pi 4 sends the reset signal, the relay cuts power to the IO Board for 5 seconds.

The principal is the exact same as the D1Mini solution, but the D1Mini is subsituted with the Raspberry Pi 4. If you want to run MQTT using python on a Raspberry Pi 4 these are the steps:

### Dependencies:
 - Install mosquitto service:
    - `sudo apt-get install mosquitto mosquitto-clients`
    - `sudo systemctl enable mosquitto`
    - check if mosquitto is running `sudo systemctl status mosquitto`

- Create your own mosquitto configuration file:
   - `cd /etc/mosquitto/conf.d`
   - `sudo nano YOUR_FILE_NAME.conf`
   - paste these lines for insecure connection:
        
       ```
       allow_anonymous true
        
       listener 1883
       ```
   - paste these lines for secure connection:
       
       ```
       allow_anonymous true
        
       listener 8883
        
       require_certificate true
       
       cafile /SOME/PATH/TO/ca.crt
        
       certfile /SOME/PATH/TO/server.crt
        
       keyfile /SOME/PATH/TO/server.key
       ``` 
   - Restart mosquitto service to recognize conf changes `sudo systemctl restart mosquitto.service`  
   - Check status to ensure mosquitto restarted successfully `sudo systemctl status mosquitto.service`
   - *refer to https://mosquitto.org/man/mosquitto-conf-5.html for conf file documentation*

- Install the paho.mqtt library:
   - `git clone https://github.com/eclipse/paho.mqtt.python`
   - `cd paho.mqtt.python`
   - `sudo python3 setup.py install`

- Install the GPIO package:
   - On Raspbian: `apt-get install rpi.gpio`
   - On Ubuntu: `sudo apt install python3-lgpio`
   
- Install the pytz timezone library: `pip install pytz`

- Install the pythonping library: `sudo pip install pythonping`

After installing dependencies: 

### Steps:
- Clone this repo to get necessary files `git clone https://github.com/NAU-IoT/RemotePiReset.git`
- Change into RemotePiReset directory `cd RemotePiReset`
- Change PRPConfiguration.py variable names and paths according to your implementation `nano RPRConfiguration.py`
- Verify that permissions are set so that the script is executable by typing `chmod +x RemotePiReset.py` in the command line
- To use TLS set, uncomment lines 71-73 and change 1883 to 8883 on line 76
- IF USING TLS SET: ensure keyfile has the correct permissions for the user to run the script without error
   - If getting error "Error: Problem setting TLS options: File not found." use command `sudo chmod 640 YourKeyFile.key` (sets permissions so that the user and group are able to read the keyfile)    
- Type `./RemotePiReset.py` into the command line to execute the script
   - Can also use `python3 RemotePiReset.py`
- Publish reset command to topic from client using command:
   
   WITHOUT TLS: `mosquitto_pub -p 1883 -t YOUR_TOPIC -h YOUR_BROKER_IP -m "reset"`
   
   WITH TLS: `mosquitto_pub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -d -h YOUR_BROKER_IP -t YOUR_TOPIC -m "reset"`

- Done!


### Implementing the script as a service
  
  - Create a systemd entry 
      - Change into Systemctl directory `cd RemotePiReset/Systemctl` 
      - Modify line 8 of RemotePiReset.service to reflect the correct path `nano RemotePiReset.service`
      - Copy the .service file to correct location `sudo cp RemotePiReset.service /etc/systemd/system`
  - Create logs directory inside of the RemotePiReset directory `mkdir logs`
  - Modify RemotePiReset.sh to include the correct paths (located inside of the Systemctl directory) `nano RemotePiReset.sh`
  - Set file permissions for RemotePiReset.sh `sudo chmod 744 RemotePiReset/Systemctl/RemotePiReset.sh`
      - If this step is unsuccessful, here are potential solutions:
         - Change permissions further `sudo chmod 755 RemotePiReset/Systemctl/RemotePiReset.sh`
         - Change permissions for the directory as well `sudo chmod 755 RemotePiReset`
  - Enable the service 
      - `sudo systemctl daemon-reload`
      - `sudo systemctl enable RemotePiReset.service`
      
  - Start the service `sudo systemctl start RemotePiReset.service`
  
  - Check the status of the service `sudo systemctl status RemotePiReset.service`
  
  - Done! The service should now run on boot. 
         
      

