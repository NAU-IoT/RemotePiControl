# RemotePiReset
This repository contains code to be uploaded onto a D1 Mini Pro to facilitate a remote reset on a RaspberryPi. 

This solution can also be done using a RaspberryPiZero, which is also documented here.

# Components:

**D1MINI PRO**

    Used to interpret reset command over MQTT and send resetting signal to relay
    
**RASPBERRY PI**

    Wired through the relay, this is what is being reset
    
**5V RELAY**

    Wired so that when the D1Mini sends the reset signal, the relay cuts power to the Rpi for 5 seconds.
    
    
# RaspberryPIZero Solution

If you want to run the code on a RaspberryPi Zero these are the steps:

- SSH into the Rpi Zero
- Create a new script using nano (or any text editor)
- Write in source code (found repository under PiZero Method)
- Save your <YourFile>.c
- Compile using:    gcc <YourFile>.c
- If there are no errors, specify executable file:  gcc <YourFile>.c  -o <YourFile>
- Verify that the file is executable (permissions)
- Run file by using ./<YourFile>

