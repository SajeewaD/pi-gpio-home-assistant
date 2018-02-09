import RPi.GPIO as GPIO
import time
import sys
import signal
import requests 
import json

#Configuration:

#GPIO Pin used to read door sensor
DOOR_SENSOR_PIN = 18

#Home Assistant URL
HOME_ASSISTANT_URL = "http://parrot:8123"
HOME_ASSISTANT_PASSWORD = ""
HA_SENSOR_NAME = "garagedoor"
HA_SENSOR_FRIENDLY_NAME = "Garage Door"

def notifyHomeAssistant(state):

    if ( state != "open" and state != "closed"):
        print "Unknown state passed to notifyHomeAssistant - " + state
        return

    icon = "mdi:garage"

    if ( state == "open" ):
        icon = "mdi:garage-open"

    post_url = "{server}/api/states/binary_sensor.{name}".format( server = HOME_ASSISTANT_URL, name = HA_SENSOR_NAME)

    response = requests.post(post_url, headers={'x-ha-access': HOME_ASSISTANT_PASSWORD, 'content-type': 'application/json'},
        data=json.dumps({'state': state, 'attributes': {'friendly_name': HA_SENSOR_FRIENDLY_NAME, 'icon': icon}}))

    print(response.text) # For debugging

# Clean up when the user exits with keyboard interrupt
def cleanup(signal, frame): 
    GPIO.cleanup() 
    sys.exit(0)

# Start of programme    
if __name__ == "__main__":

    # Set board mode so we can address GPIO pins by number.
    GPIO.setmode(GPIO.BOARD) 

    # Initially we don't know if the door sensor is open or closed...
    isOpen = None
    oldIsOpen = None 

    # Set up the door sensor pin, use the build in pull down
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) 

    # Set the cleanup handler for when user hits Ctrl-C to exit
    signal.signal(signal.SIGINT, cleanup) 

    while True: 
        oldIsOpen = isOpen 
        isOpen = GPIO.input(DOOR_SENSOR_PIN)

        if ( isOpen != oldIsOpen ):
            if (isOpen):
                print "Door is Open"
                notifyHomeAssistant("open")
            else:
                print "Door is Closed"
                notifyHomeAssistant("closed")
    
        # Keep this relatively long to handle debounce so the sensor
        # doesn't flicker between the two states
        time.sleep(1)
