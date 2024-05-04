import RPi.GPIO as GPIO
import time

servoButA = 26
servoButB = 32
extraButC = 37

relIn1 = 8
relIn2 = 10
relIn3 = 12

motInA = 16
motInB = 18
enA = 38
enB = 40

limSwA = 22
limSwB = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(servoButA, GPIO.OUT)
GPIO.setup(servoButB, GPIO.OUT)
GPIO.setup(extraButC, GPIO.OUT)

GPIO.setup(relIn1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relIn2, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relIn3, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(limSwA, GPIO.IN)
GPIO.setup(limSwB, GPIO.IN)

GPIO.setup(motInA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motInB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
pwmA = GPIO.PWM(enA, 1000)
pwmB = GPIO.PWM(enB, 1000)
pwmA.start(45)
pwmB.start(45)



while True:


    GPIO.output(servoButB, GPIO.HIGH)
    GPIO.output(servoButA, GPIO.LOW)
    GPIO.output(extraButC, GPIO.HIGH)

    # GPIO.output(relIn1, GPIO.LOW)
    # GPIO.output(relIn2, GPIO.LOW)
    # GPIO.output(relIn3, GPIO.LOW)
    

    if GPIO.input(limSwA) == 0:
        pwmA.ChangeDutyCycle(65)
        pwmB.ChangeDutyCycle(65)
        GPIO.output(motInA, GPIO.LOW)
        GPIO.output(motInB, GPIO.HIGH)
    else:
        GPIO.output(motInA, GPIO.LOW)
        GPIO.output(motInB, GPIO.LOW)


# toShort


    # if GPIO.input(limSwB) == 0:
    #     pwmA.ChangeDutyCycle(45)
    #     pwmB.ChangeDutyCycle(45)
    #     GPIO.output(motInA, GPIO.HIGH)
    #     GPIO.output(motInB, GPIO.LOW)
    # else:
    #     GPIO.output(motInA, GPIO.LOW)
    #     GPIO.output(motInB, GPIO.LOW)




# GPIO.cleanup()