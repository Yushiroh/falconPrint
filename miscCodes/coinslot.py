import RPi.GPIO as GPIO
import time
coinPin = 8
coinPulse = []
import pygame
pulseTimerState = False
pulseTimer = 0

pulseCounter = 0
changeCounter = 0


GPIO.setmode(GPIO.BOARD)
GPIO.setup(coinPin, GPIO.IN)    

while True:

    pulse = GPIO.input(coinPin)


    if pulse == 0:
        pulseCounter += 1
        pulseTimerState = True

    if pulseTimerState:
        pulseTimer += 1

    if pulseTimer > 60:
        coinPulse.append(pulseCounter)
        


        pulseTimerState = False
        pulseTimer = 0
        pulseCounter = 0

        print(f"change counter = {changeCounter}")
        # changeCounter = 0

    for pulses in coinPulse:
        if pulses != 61:
            changeCounter += 1
    
    
    

        