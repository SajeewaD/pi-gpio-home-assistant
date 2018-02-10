# pi-gpio-home-assistant

## Installation
* Copy run_doorsensor.sh and garage-door.py to a location of your choosing
* copy doorsensor to /etc/init.d/ so it can be accessed via /etc/init.d/doorsensor

## Configuration
* garage-door.py - update GPIO pins and Home Assistant configuration within the file
* run_door_sensor.sh - update the path to the python file
* doorsensor - update the path to run_door_sensor.sh

## Running the service
simple type 
sudo /etc/init.d/doorsensor start