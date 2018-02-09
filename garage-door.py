import RPi.GPIO as GPIO
import time
import sys
import signal 

# Set board mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BOARD) 

#GPIO Pin used to read door sensor
DOOR_SENSOR_PIN = 18

# Clean up when the user exits with keyboard interrupt
def cleanup(signal, frame): 
    GPIO.cleanup() 
    sys.exit(0)


# Start of programme    
if __name__ == "__main__":

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
            else:
                print "Door is Closed"
    
        # Keep this relatively long to handle debounce so the sensor
        # doesn't flicker between the two states
        time.sleep(1)
