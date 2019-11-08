# minibot sonar avoider 2 stepper
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
minibot sonar avoider 2 stepper
===========================================================

Author(s):  Don Korte
Repository: https://github.com/dnkorte/minibot

ItsyBitsy pin connections:
        12:     Left Servo 
        11:     Right Servo 
        10:     HC-s04 Trigger
        9:      HC-s04 Echo
        7:      PB 1
        5:      NeoPixel
        1:      PB 2
        0:      
        2:      
        A5:     piezo
"""
import time
import board
import digitalio
import pulseio
from adafruit_motor import servo
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

# create a PWMOut object on Pin D12 and D11
pwmL = pulseio.PWMOut(board.D12, frequency=50)
pwmR = pulseio.PWMOut(board.D11, frequency=50)

# Create a servo object, left_servo.
left_servo = servo.ContinuousServo(pwmL)
right_servo = servo.ContinuousServo(pwmR)

# create object for sonar device
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D10, echo_pin=board.D9, timeout=1.0)

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

# note throttle range is 1.0 -> -1.0
side_throttle = 1.0
side_duration = 8
turn_duration = 0.8
turn_throttle = 0.5

for i in range(10):
    drive(side_duration)
    turn_right(turn_throttle, turn_duration)

# all done, so bow and quit
spin_right(4)