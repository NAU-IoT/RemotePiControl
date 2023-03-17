#!/bin/bash

# cd /code/python/myapp
python3 /RemotePiControl.py >> /Data/logs/RemotePiControl-`date '+%Y%m%d'`.log 2>&1
