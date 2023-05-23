#!/bin/bash

# Find the process ID of the running RemotePiControl script
pid=$(pgrep -f RemotePiControl.py)

# Kill the process if it is running
if [ -n "$pid" ]; then
  kill "$pid"
fi

python3 /RemotePiControl.py >> /Data/logs/RemotePiControl-`date '+%Y%m%d'`.log 2>&1
