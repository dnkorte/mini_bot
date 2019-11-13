# minibot simple demo
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
ItsyBitsy pin connections:
        12:     Left Servo
        11:     Right Servo

Libraries needed:
    adafruit_bus_device
    adafruit_motor
    adafruit_button
    adafruit_dotstar
==========================================================       
"""

import time
import board
import pulseio
from adafruit_motor import servo

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


# create a PWMOut object on Pin D12 and D11
pwmL = pulseio.PWMOut(board.D12, frequency=50)
pwmR = pulseio.PWMOut(board.D11, frequency=50)

# Create a servo object, left_servo.
left_servo = servo.ContinuousServo(pwmL)
right_servo = servo.ContinuousServo(pwmR)

# startup delay
time.sleep(2)

# note throttle range is 1.0 -> -1.0
side_throttle = 1.0
side_duration = 2.2
turn_duration = 0.5
turn_throttle = 0.5

forward(side_throttle, side_duration)
turn_right(turn_throttle, turn_duration)
forward(side_throttle, side_duration)
turn_right(turn_throttle, turn_duration)
forward(side_throttle, side_duration)
turn_right(turn_throttle, turn_duration)
forward(side_throttle, side_duration)
spin_left(4)

seesaw_throttle = 0.3
seesaw_duration = 2
forward(seesaw_throttle, seesaw_duration)
backward(seesaw_throttle, seesaw_duration)
forward(seesaw_throttle, seesaw_duration)
backward(seesaw_throttle, seesaw_duration)
forward(seesaw_throttle, seesaw_duration)
backward(seesaw_throttle, seesaw_duration)
spin_right(4)

# dp a wheelie
backward(1.0, 0.5)


