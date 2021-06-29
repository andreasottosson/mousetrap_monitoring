# -*- coding: utf-8 -*-
# A simple python script for monitoring mouse traps using a Raspberry Pi
# Using Button / when_released for simplicity, could be made nicer I guess
# Written by Andreas Ottosson (https://github.com/andreasottosson)

from gpiozero import Button
from signal import pause
import os
import sys
import requests

# Where is the traps connected on the Pi, there is one wire to the GPIO and one to ground and when that connection is broken ie the trap has sprung it triggeres when_released
trap_gpio_pins = [2,3,4,5,6,13,19,26] 

traps = []

try:
    os.environ["IFTT_KEY"]
except KeyError:
    print("Please set the environment variable IFTT_KEY")
    sys.exit(1)

# Save basic stats in a text file
def trap_stats(t):
    file = open('trap_stats.txt', 'a')
    file.write(t+'\n')
    file.close()

def trap_setup():
    for p in trap_gpio_pins:
        count = 1

        globals()['trap'+str(count)] = Button(p, bounce_time=5)
        globals()['trap'+str(count)].when_released = trap_triggered
        traps.append(globals()['trap'+str(count)])

        count = count + 1

def gpio_to_trap(pin):
    gpio = str(pin).strip('GPIO') # pin = GPIO17 etc...
    trap_nr = trap_gpio_pins.index(int(gpio))
    trap_nr = trap_nr + 1
    return f'trap{trap_nr}'

def trap_triggered(button_object):
    t = gpio_to_trap(button_object.pin)
    post_body = {'value1': t}
    print(f'Trap {t} got triggered!')

    trap_stats(t)

    try:
        # Sends notifications using the IFTT action "trap_triggered", create on your own account to get a valid key
        r = requests.post('https://maker.ifttt.com/trigger/trap_triggered/with/key/{}'.format(os.environ["IFTT_KEY"]), json=post_body)
        print('Notification sent to IFTTT')
        print(r)
    except requests.exceptions.RequestException as e:
        print('Error sending notification to IFTTT')
        print(e)

def check_traps():
    unarmed_trap = False

    for trap in traps:
        if trap.value != 1:
            unarmed_trap = True
            t = gpio_to_trap(trap.pin)
            print(f'Trap {t} is not armed!')

    if unarmed_trap == True:
        print('WARNING! Some traps are not armed.')
    else:
        print('All traps are armed and ready!')

trap_setup()

check_traps()

pause() # Leave program running...
