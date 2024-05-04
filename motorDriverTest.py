import RPi.GPIO as GPIO
import time

motInA = 16
motInB = 18
enA = 38
enB = 40

limSwA = 22
limSwB = 24

servoButA = 26
servoButB = 32

relIn1 = 8
relIn2 = 10
relIn3 = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(motInA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(motInB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
pwmA = GPIO.PWM(enA, 1000)
pwmB = GPIO.PWM(enB, 1000)
pwmA.start(50)
pwmB.start(50)
GPIO.setup(servoButA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(servoButB, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(relIn1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relIn2, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relIn3, GPIO.OUT, initial=GPIO.HIGH)



GPIO.setup(limSwA, GPIO.IN)
GPIO.setup(limSwB, GPIO.IN)
# GPIO.cleanup()

GPIO.output(servoButA, GPIO.LOW)
GPIO.output(servoButB, GPIO.LOW)
print(GPIO.output(servoButA, GPIO.LOW))
time.sleep(3)

GPIO.output(servoButA, GPIO.HIGH)
print(GPIO.output(servoButA, GPIO.HIGH))
GPIO.output(servoButB, GPIO.HIGH)
# GPIO.cleanup()

# while True:
  
#    GPIO.output(relIn1, GPIO.LOW)
#    GPIO.output(relIn2, GPIO.LOW)
#    GPIO.output(relIn3, GPIO.LOW)

    # if GPIO.input(limSwB) == 0:
    #     GPIO.output(motInA, GPIO.HIGH)
    #     GPIO.output(motInB, GPIO.LOW)
    # else:
    #     GPIO.output(motInA, GPIO.LOW)
    #     GPIO.output(motInB, GPIO.LOW)
    

    # if GPIO.input(limSwA) == 0:
    #     GPIO.output(motInA, GPIO.LOW)
    #     GPIO.output(motInB, GPIO.HIGH)
    # else:
    #     GPIO.output(motInA, GPIO.LOW)
    #     GPIO.output(motInB, GPIO.LOW)
    

       

       

#to short 
#    GPIO.output(motInA, GPIO.HIGH)
#    GPIO.output(motInB, GPIO.LOW)

# to long
#    GPIO.output(motInA, GPIO.LOW)
#    GPIO.output(motInB, GPIO.HIGH)

    # time.sleep(3)

    # GPIO.output(relIn3, GPIO.HIGH)

    # print("A: ")
    # print(GPIO.input(limSwA))

    # print("----")
 
    # print("B: ")
    # print(GPIO.input(limSwB))




#     GPIO.output(motInA, GPIO.LOW)
#     GPIO.output(motInB, GPIO.HIGH)
    
#     # time.sleep(3)
    
#     GPIO.output(motInA, GPIO.HIGH)
#     GPIO.output(motInB, GPIO.LOW)








