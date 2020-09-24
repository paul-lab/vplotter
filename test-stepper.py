'''
Use this to check your stepper motor hat/bonnet and that you have the motors
on the correct side and wired up correctly

Motor 1 is the left hand motor, when facing the canvas, connected to M1 & M2
Motor 2 is the right hand motor, when facing the canvas, connected to M3 & M4

https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi
'''


import time
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit
 
kit = MotorKit()

input ("'Enter' to continue")
print ("Both motors turning OUTWARDS, raising the point of the V for 1 revolution")
for i in range(200):
    kit.stepper1.onestep(direction=STEPPER.FORWARD, style=STEPPER.SINGLE)
    kit.stepper2.onestep(direction=STEPPER.BACKWARD, style=STEPPER.SINGLE)
    time.sleep(0.02)

input ("'Enter' to continue")
print ("Both motors turning INWARDS. lowering the point of the V for 1 revolution")
for i in range(200):
    kit.stepper1.onestep(direction=STEPPER.BACKWARD, style=STEPPER.SINGLE)
    kit.stepper2.onestep(direction=STEPPER.FORWARD, style=STEPPER.SINGLE)
    time.sleep(0.02)


#releases  the coils so the motor can free spin, and also won't use any power
kit.stepper1.release()
kit.stepper2.release()
print ("Motors released")
