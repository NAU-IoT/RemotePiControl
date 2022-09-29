# RemotePiReset
This repository contains code to be uploaded onto a D1 Mini Pro to facilitate a remote reset on a RaspberryPi.

Components:

D1MINI PRO
    Used to interpret reset command over MQTT and send resetting signal to relay
    
RASPBERRY PI
    Wired through the relay, this is what is being reset
    
5V RELAY
    Wired so that when the D1Mini sends the reset signal, the relay cuts power to the Rpi for 5 seconds.
    
    
    
If you want to run the code on a RaspberryPi Zero these are the steps:

- ssh into the Rpi Zero
- 
