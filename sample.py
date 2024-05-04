import RPi.GPIO as GPIO
import time


servoButA = 26
servoButB = 32

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoButA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(servoButB, GPIO.OUT, initial= GPIO.LOW)


# GPIO.output(servoButA, GPIO.HIGH)
# GPIO.output(servoButB, GPIO.LOW)

# GPIO.cleanup()
# while True:

    #low high short
    #high high long
GPIO.output(servoButA, GPIO.HIGH)
GPIO.output(servoButB, GPIO.HIGH)
time.sleep(3)
    # GPIO.cleanup()
    # print(GPIO.output(servoButA, GPIO.HIGH))
    


# GPIO.output(servoButA, GPIO.HIGH)
# print(GPIO.output(servoButA, GPIO.HIGH))
# GPIO.output(servoButB, GPIO.HIGH)