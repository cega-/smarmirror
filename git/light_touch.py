import sys
import time

import board
import busio

##import Adafruit_MPR121.MPR121 as MPR121
# Import MPR121 module.
import adafruit_mpr121 as MPR121
import RPi.GPIO as GPIO

# GPIO_22 Relay 2
# GPIO_27 Relay 1

print('Adafruit MPR121 Capacitive Touch Sensor Test')

# Create MPR121 instance.
##cap = MPR121.MPR121()
# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

cap = MPR121.MPR121(i2c)

#if not cap.begin():
#    print('Error initializing MPR121.  Check your wiring!')
#    sys.exit(1)

# Main loop to print a message every time a pin is touched.
print('Press Ctrl-C to quit.')
last_touched = cap.touched()
l_press_touch = []
while True:
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            if i not in l_press_touch:
              l_press_touch.append(i)
              if i == 11:
               	GPIO.setmode(GPIO.BCM)
               	GPIO.setup(22, GPIO.OUT)
               	GPIO.output(22, GPIO.LOW)
              if i == 0:
               	GPIO.setmode(GPIO.BCM)
               	GPIO.setup(27, GPIO.OUT)
               	GPIO.output(27, GPIO.LOW)
            else:
               l_press_touch.remove(i)
               if i == 11:
               	GPIO.output(22, GPIO.HIGH)
               if i == 0:
               	GPIO.output(27, GPIO.HIGH)
        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)
GPIO.cleanup()
