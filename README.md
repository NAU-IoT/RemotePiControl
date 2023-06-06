# RemotePiControl
This repository contains code to facilitate a remote reset, remote stop, remote start, or status message on a RaspberryPi. 

This solution can also be done using a D1MiniPro. The D1MiniPro solution is not fully developed, and can only implement the reset function. You can find this solution documented here: https://github.com/NAU-IoT/D1Mini-RemotePiReset 

## Components:

**Raspberry Pi 4**

   Used to interpret reset command over MQTT and send signal to relay
    
**RASPBERRY PI IO Board**

   Wired through the relay, this is what is being controlled
    
**RELAY**

   Wired so that when the Pi 4 sends a signal, the relay cuts or allows power to the IO Board:
   
   - Cut power for 5 seconds (reset)
      
   - Indefinitely cut power (stop)
      
   - Indefinitely allow power (start)

A normal standalone relay is fine for use, but the relay hat can be found here: https://www.amazon.com/gp/product/B07CZL2SKN/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1


# Running with Docker

- Install docker: 
```
sudo apt install docker.io 
```

- Check if docker is functioning: 
```
sudo docker run hello-world
```  
- Clone repository to get Dockerfile and configuration files: 
```
git clone https://github.com/NAU-IoT/RemotePiControl.git
```
- Change into docker directory: 
```
cd RemotePiControl/rpc-docker
```
- Modify RPCConfiguration.py to match your current implementation: 
   - Refer to comments for necessary changes
```
nano RPCConfiguration.py
```
- OPTIONAL: To change the docker containers time zone, edit line 33 in the Dockerfile. A list of acceptable time zones can be found at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones 
- Build docker image in current directory:
   - This will take a while
```
docker build -t remotepicontrol .
```
- Create a directory in a convenient location to store the docker volume. For example: 
```
mkdir -p Data/RPCData
```
- Create a volume to store data inside the directory created in the previous step: 
```docker volume create --driver local 
    --opt type=none 
    --opt device=/SOME/LOCAL/DIRECTORY 
    --opt o=bind 
    YOUR_VOLUME_NAME
```
- Execute docker container: 
    - Note for IoT Team: Your_port_number could be 11883, container_port_number should be 31883
```
docker run --privileged -v YOUR_VOLUME_NAME:/Data -p YOUR_PORT_NUMBER:CONTAINER_PORT_NUMBER -t -i -d --restart unless-stopped remotepicontrol
```

- Verify container is running: 
```
docker ps
```
- Done!
 
 ## Notes
 - To publish commands to topic from client, use command:
   
   WITHOUT TLS: 
   
   IoT Team: PORT_NUMBER should be 31883 (number in RPCConfiguration.py)
   ```
   mosquitto_pub -p PORT_NUMBER -t YOUR_TOPIC -h YOUR_BROKER_IP -m "reset/start/stop/status"
   ```
   
   Example command:
   ```
   mosquitto_pub -p 1883 -t HomeNetwork -h localhost -m "reset"
   ```
   
   WITH TLS: 
   ```
   mosquitto_pub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -d -h YOUR_BROKER_IP -t YOUR_TOPIC -m "reset/start/stop/status"
   ```
   Example command:
   ```
   mosquitto_pub --cafile /home/michael/cafile.crt --cert /home/michael/certfile.crt --key /home/michael/keyfile.key -p 8883 -d -h localhost -t HomeNetwork -m "reset"
   ```
  
 - To enter the container:
   - This can be done to check log files or modify the container without rebuilding
 ```
 docker exec -it CONTAINER_ID /bin/bash
 ```

## Common Errors
 
  - If error: `Got permission denied while trying to connect to the Docker daemon socket at unix ... connect: permission denied`
    - Run command: 
    ```
    sudo usermod -aG docker $USER
    ```
    - Log out and ssh back into system


# Running with Python and Systemctl  

## Dependencies:
 - Install mosquitto service:
    ```
    sudo apt-get install mosquitto mosquitto-clients
    ```
    
    ```
    sudo systemctl enable mosquitto
    ````
 - Check if mosquitto is running:
    ```
    sudo systemctl status mosquitto
    ```

- Create your own mosquitto configuration file:
   ```
   cd /etc/mosquitto/conf.d
   ```
   
   ```
   sudo nano YOUR_FILE_NAME.conf
   ```
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
   - Restart mosquitto service to recognize conf changes: 
   ```
   sudo systemctl restart mosquitto.service
   ```  
   - Check status to ensure mosquitto restarted successfully: 
   ```
   sudo systemctl status mosquitto.service
   ```
   - *refer to https://mosquitto.org/man/mosquitto-conf-5.html for conf file documentation*

- Install the paho.mqtt library:
   ```
   git clone https://github.com/eclipse/paho.mqtt.python
   ```
   ```
   cd paho.mqtt.python
   ```
   ```
   sudo python3 setup.py install
   ```

- Install the GPIO package:
   - On Raspbian: 
   ```
   sudo apt-get install rpi.gpio
   ```
   - On Ubuntu: 
   ```
   sudo apt install python3-lgpio
   ```
   
- Install the pytz timezone library: 
```
pip install pytz
```

- Install the pythonping library: 
```
sudo pip install pythonping
```

After installing dependencies: 

## Steps:

- Clone this repo to get necessary files: 
```
git clone https://github.com/NAU-IoT/RemotePiControl.git
```
- Change into RemotePiControl directory: 
```
cd RemotePiControl
```
- Change RPCConfiguration.py variable names and paths according to your implementation: 
```
nano RPCConfiguration.py
```
- Verify that permissions are set so that the script is executable by running: 
```
chmod +x RemotePiControl.py
```
- To use TLS set, uncomment lines 192-194 in RemotePiControl.py and change Port to 8883 in RPCConfiguration.py
- IF USING TLS SET: ensure keyfile has the correct permissions for the user to run the script without error
   - If getting error "Error: Problem setting TLS options: File not found." use command:
     - (sets permissions so that the user and group are able to read the keyfile) 
   ```
   sudo chmod 640 YourKeyFile.key
   ```
- Execute the script:
```
./RemotePiControl.py
```
   - Can also use: 
   ```
   python3 RemotePiControl.py
   ```
- Publish reset command to topic from client using command:
   
   WITHOUT TLS: 
   
   ```
   mosquitto_pub -p PORT_NUMBER -t YOUR_TOPIC -h YOUR_BROKER_IP -m "reset/start/stop/status"
   ```
   
   example command:
   ```
   mosquitto_pub -p 1883 -t HomeNetwork -h localhost -m "reset"
   ```
   
   WITH TLS: 
   ```
   mosquitto_pub --cafile YOUR_CAFILE.crt --cert YOUR_CERTFILE.crt --key YOUR_KEYFILE.key -p 8883 -d -h YOUR_BROKER_IP -t YOUR_TOPIC -m "reset/start/stop/status"
   ```
   example command:
   ```
   mosquitto_pub --cafile /home/michael/cafile.crt --cert /home/michael/certfile.crt --key /home/michael/keyfile.key -p 8883 -d -h localhost -t HomeNetwork -m "reset"
   ```

- Done!


## Implementing the script as a service

Note: If using standalone relay rather than relay hat, change "26" to "4" on line 30 of RemotePiControl.py and hook your signal jumper up to pin 7 of the pi4.

  - Create logs directory inside of the RemotePiControl directory: 
  ```
  mkdir logs
  ```
  - Create a systemd entry 
      - Change into Systemctl directory: 
      ```
      cd RemotePiControl/Systemctl
      ``` 
      - Modify line 9 of RemotePiControl.service to reflect the correct path: 
      ```
      nano RemotePiControl.service
      ```
      - Copy the .service file to correct location: 
      ```
      sudo cp RemotePiControl.service /etc/systemd/system
      ```
  - Modify RemotePiControl.sh to include the correct paths (located inside of the Systemctl directory): 
  ```
  nano RemotePiControl.sh
  ```
  - Set file permissions for RemotePiControl.sh: 
  ```
  sudo chmod 744 RemotePiControl/Systemctl/RemotePiControl.sh
  ```
  - If previous step is unsuccessful, here are potential solutions:
     - Change permissions further: 
     ```
     sudo chmod 755 RemotePiControl/Systemctl/RemotePiControl.sh
     ```
     - Change permissions for the directory as well: 
     ```
     sudo chmod 755 RemotePiControl
     ```
  - Enable the service: 
      ```
      sudo systemctl daemon-reload
      ```
      ```
      sudo systemctl enable RemotePiControl.service
      ```
      
  - Start the service: 
  ```
  sudo systemctl start RemotePiControl.service
  ```
  
  - Check the status of the service: 
  ```
  sudo systemctl status RemotePiControl.service
  ```
  
  - Done! The service should now run on boot. 
         
    
  ## Common Errors
  
  `socket.gaierror: [Errno -2] Name or service not known`
  
   - Most likely an issue with the DNS name or IP address not being recognized
  

      

