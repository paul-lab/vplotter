'''
    Test the servo for the pen lifter.

    remember to 'sudo pigpiod'  or have it run at startup
    
    The pulse frequency should be no higher than 100Hz - higher values could (WILL) damage the servos
    This is the Broadcom gpio pin (18) we are using for the servo (pen lifter)

    u - up
    d - down
    q - quit
'''

import time
import pigpio

lastPenup = False

# instantiate this Raspberry Pi as a pigpio.pi() instance
rpi = pigpio.pi()

# the pulse frequency should be no higher than 100Hz - higher values could (supposedly) damage the servos
rpi.set_PWM_frequency(18, 50)


def set_pen_up(PenUp=True):
    '''
        Dont underestimate how violent these servos are, they throw the
        pen carriage all over the place. The difficulty is balancing the
        unwanted movement and the time taken to lift or drop the pen,
        especially with a busy drawing (not a good idea anyway)

        You are much better off moving the pen rather than the entire carriage

        The idea is to keep the movement (difference between up and down)
        as small as possible and dampen it if we can

        if you are lifting the pen rather than the  carriage, the loop could
        probably be sped up a little
    '''
    global lastPenup
    if lastPenup == PenUp:
        return()
    else:
        lastPenup = PenUp
    
    up = 1800      
    down = 1450
    gpio_pin=18
    transition_time = 0.02
    
    if PenUp == True:
        for i in range(down,up+20,20):
            time.sleep(transition_time)
            rpi.set_servo_pulsewidth(gpio_pin, up)  
    else:
        for i in range(up,down-20,-20):
            time.sleep(transition_time)
            rpi.set_servo_pulsewidth(gpio_pin, down)


set_pen_up(False)
set_pen_up(True)
while 1 == 1:
    pup = input ("(U)p, (D)own   or (Q)uit? ")
    pup = pup.upper()
    if pup == "U":
        set_pen_up(True)
    elif pup == "D":
        set_pen_up(False)
    elif pup == "Q":
        exit()
