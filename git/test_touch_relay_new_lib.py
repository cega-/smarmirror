import time
import board
import busio

# Import MPR121 module.
import adafruit_mpr121

import RPi.GPIO as GPIO

# GPIO_22 Relay 2
# GPIO_27 Relay 1

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

# Note you can optionally change the address of the device:
#mpr121 = adafruit_mpr121.MPR121(i2c, address=0x91)

last_touched = mpr121.touched()
l_press_touch = []

while True:
    current_touched = mpr121.touched()
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
               GPIO.setmode(GPIO.BCM)
               GPIO.setup(22, GPIO.OUT)
               GPIO.output(22, GPIO.LOW)
            else:
               l_press_touch.remove(i)
               GPIO.output(22, GPIO.HIGH)
               GPIO.cleanup()
        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)
