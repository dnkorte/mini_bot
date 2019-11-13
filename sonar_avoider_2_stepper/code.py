# minibot sonar avoider 2 stepper
# 
# Author(s):  Don Korte
# github: https://github.com/dnkorte/mini_bot.git
# 
# MIT License
# 
# Copyright (c) 2019 Don Korte
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

"""
===========================================================

NOTE that this program requires an M4 class processor due to memory usage
NOTE ALSO: the geared down amazon stepper motor is WAY too slow to make this useful !!

ItsyBitsy pin connections:
        12:     (Left Servo) 
        11:     (Right Servo) 
        10:     HC-s04 Trigger
        9:      
        7:      HC-s04 Echo
        5:      NeoPixel
        1:      
        0:      
        2:      
        A5:     piezo
        SCL:    to SCL on Stepper Featherwing (yellow)
        SDA:    to SDA on Stepper Featherwing (blue)

NeoPixel connection:
        DataIn: to pin 5 on ItsyBitsy (yellow)
        +5v:    to +5v from battery (red)
        GND:    to ground (black)
        (note that 3 pin header is in order yellow, red, black)

Stepper Featherwing connections 
        VBAT:   to +5v from battery (red)
        +3V:    to 3v bus (sourced by ItsyBitsy 3v pin) (orange)
        GND:    to ground (black) (note be sure to jumper the logic gnd and motor gnd on board)
        SCL:    to SCL on ItsyBitsy (yellow)
        SDA:    to SDA on SItsyBitsy (blue)
        (note that 5 pin header is in order: red, orange, black, blue, yellow)
        Left Stepper: to M1/M2
        Right Stepper: to M3/M4

Libraries needed:
    adafruit_bus_device (folder)
    adafruit_motor (folder)
    adafruit_register (unique to stepper version) (folder)
    adafruit_button
    adafruit_dotstar
    adafruit_hcsr04
    adafruit_motorkit (unique to stepper version)
    adafruit_pca9685 (unique to stepper version)
    neopixel
===========================================================
"""

import time
import board
import digitalio
import pulseio
# from adafruit_motor import servo
from adafruit_motorkit import MotorKit
# from adafruit_motor import stepper
import adafruit_hcsr04
import random
import neopixel

def drive(seconds):
    for i in range(seconds * 10):
        left_servo.throttle = 1
        right_servo.throttle = -1
        neopixels[0] = (0, 255, 0)
        neopixels[1] = (0, 255, 0)
        neopixels[4] = (0, 255, 0)
        neopixels.show()
        if check_sonar() < 10:
            # if saw something close, then backup for a while
            left_servo.throttle = -1
            right_servo.throttle = 1
            neopixels[0] = (255, 0, 0)
            neopixels[1] = (255, 0, 0)
            neopixels[4] = (255, 0, 0)
            neopixels.show()
            time.sleep(1)
            # then go forward and turn a little bit with turn in random direction
            if (random.randint(0,10) > 4):
                left_servo.throttle = 1
                right_servo.throttle = 1
                neopixels[0] = (255, 255, 0)
                neopixels[1] = (255, 255, 0)
                neopixels[4] = (255, 255, 0)
                neopixels[2] = (255, 255, 0)
                neopixels[3] = (255, 255, 0)
            else:
                left_servo.throttle = -1
                right_servo.throttle = -1
                neopixels[0] = (0, 0, 255)
                neopixels[1] = (0, 0, 255)
                neopixels[4] = (0, 0, 255)
                neopixels[5] = (0, 0, 255)
                neopixels[6] = (0, 0, 255)
            neopixels.show()
            time.sleep(0.5)
            neopixels[2] = (0, 0, 0)
            neopixels[3] = (0, 0, 0)
            neopixels[5] = (0, 0, 0)
            neopixels[6] = (0, 0, 0)

        time.sleep(0.1)

def forward(throttle, seconds):
    left_servo.throttle = throttle
    right_servo.throttle = -throttle
    time.sleep(seconds)

def backward(throttle, seconds):
    left_servo.throttle = -throttle
    right_servo.throttle = throttle
    time.sleep(seconds)


def turn_right(throttle, seconds):
    left_servo.throttle = throttle
    right_servo.throttle = 0
    time.sleep(seconds)

def turn_left(throttle, seconds):
    left_servo.throttle = 0
    right_servo.throttle = throttle
    time.sleep(seconds)

def spin_left(seconds):
    left_servo.throttle = -0.5
    right_servo.throttle = -0.5
    time.sleep(seconds)

def spin_right(seconds):
    left_servo.throttle = 0.5
    right_servo.throttle = 0.5
    time.sleep(seconds)

def beep(duration):
    beeper.value = True
    time.sleep(duration)
    beeper.value = False

def check_sonar():
    try: 
        x = sonar.distance
    except RuntimeError:
        x = 999
    return x

# setup beeper
beeper = digitalio.DigitalInOut(board.A5)
beeper.direction = digitalio.Direction.OUTPUT
beeper.value = False

# setup stepper drivers
kit = MotorKit(steppers_microsteps=2)

# create object for sonar device
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D10, echo_pin=board.D7, timeout=1.0)

# setup for NeoPixels (RGB) ########################################################
NUMPIXELS = 7
ORDER = neopixel.GRB
neopixels = neopixel.NeoPixel(board.D5, NUMPIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)

# startup delay
for i in range(5):
    neopixels[i+2] = (255, 255, 0)
    neopixels.show()
    beep(0.25)
    time.sleep(0.75)

# user is ready, so turn off all the neopixels 
for i in range(NUMPIXELS):      
    neopixels[i] = (0, 0, 0)
neopixels.show()

# Constants that specify the direction and style of steps.
FORWARD = const(1)
"""Step forward"""
BACKWARD = const(2)
""""Step backward"""
SINGLE = const(1)
"""Step so that each step only activates a single coil"""
DOUBLE = const(2)
"""Step so that each step only activates two coils to produce more torque."""
INTERLEAVE = const(3)
"""Step half a step to alternate between single coil and double coil steps."""
MICROSTEP = const(4)
"""Step a fraction of a step by partially activating two neighboring coils. Step size is determined
   by ``microsteps`` constructor argument."""
# natively 5.625 degrees per step, divided by 64 gear ratio   
STEPS_PER_REV = 64 * 64

while(True):
    for i in range(STEPS_PER_REV):
        kit.stepper1.onestep(direction=FORWARD, style=SINGLE)

    for i in range(STEPS_PER_REV):
        kit.stepper1.onestep(direction=BACKWARD, style=DOUBLE)

# note throttle range is 1.0 -> -1.0
side_throttle = 1.0
side_duration = 8
turn_duration = 0.8
turn_throttle = 0.5

for i in range(10):
    # drive(side_duration)
    # turn_right(turn_throttle, turn_duration)
    pass

# all done, so bow and quit
# spin_right(4)