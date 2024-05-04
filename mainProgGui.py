import pygame
import sys
import cv2 as cv
import threading
import os
import time
from qreader import QReader
import RPi.GPIO as GPIO


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

databaseURL = 'https://fileuploading-67153-default-rtdb.asia-southeast1.firebasedatabase.app' 


cred = credentials.Certificate("fileuploading-67153-firebase-adminsdk-gn9up-59b2c4b6b9.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':databaseURL
	})

APPWIDTH, APPHEIGHT = 1024, 600 
FPS = 60
pygame.init()
pygame.display.set_caption("Final System")
sensorActivated = False
timerTickState = False
cap = cv.VideoCapture(0)
coinRead = 0


#GPIO
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



if not cap.isOpened():
    print("No cam detected")
    exit()

Black = (0,0,0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


#ASSET DECLARATIONS

mainMenu = pygame.transform.scale(pygame.image.load('guiAssets/1.jpg'), (APPWIDTH,APPHEIGHT))
ticketScanned = pygame.transform.scale(pygame.image.load('guiAssets/2.jpg'), (APPWIDTH,APPHEIGHT))
nowPrinting = pygame.transform.scale(pygame.image.load('guiAssets/3.jpg'), (APPWIDTH,APPHEIGHT))
getDocuPrompt = pygame.transform.scale(pygame.image.load('guiAssets/4.jpg'), (APPWIDTH,APPHEIGHT))
onHoldCoin = pygame.transform.scale(pygame.image.load('guiAssets/5.jpg'), (APPWIDTH,APPHEIGHT))
onHoldTap = pygame.transform.scale(pygame.image.load('guiAssets/6.jpg'), (APPWIDTH,APPHEIGHT))
topUpMode = pygame.transform.scale(pygame.image.load('guiAssets/7.jpg'), (APPWIDTH,APPHEIGHT))
topUpSuccess = pygame.transform.scale(pygame.image.load('guiAssets/8.jpg'), (APPWIDTH,APPHEIGHT))

#FONTS
dfont = pygame.font.SysFont('impact', 50)
qrFont = pygame.font.SysFont('impact', 40)
topUpFont = pygame.font.SysFont('impact',60)


def shortDispenser(paperAmt):

    print(f"paperAmount= {paperAmt}")

    for x in range(paperAmt):
        time.sleep(1)
        GPIO.output(servoButA, GPIO.HIGH)
        GPIO.output(servoButB, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(servoButA, GPIO.LOW)
        GPIO.output(servoButB, GPIO.HIGH)
        print(x)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((APPWIDTH, APPHEIGHT),pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.stateManager = stateManager('scene1')
        self.scene1 = scene1(self.screen, self.stateManager)
        self.scene2 = scene2(self.screen, self.stateManager)
        self.scene3 = scene3(self.screen, self.stateManager)
        self.scene4 = scene4(self.screen, self.stateManager)
        self.scene5 = scene5(self.screen, self.stateManager)
        self.scene6 = scene6(self.screen, self.stateManager) 
        self.scene7 = scene7(self.screen, self.stateManager)
        self.scene8 = scene8(self.screen, self.stateManager)

        self.states = {'scene1': self.scene1, 'scene2': self.scene2, 'scene3': self.scene3
                        , 'scene4': self.scene4, 'scene5': self.scene5, 'scene6': self.scene6, 'scene7': self.scene7, 'scene8': self.scene8}

    def run(self):
        while True:
            mouse = pygame.mouse.get_pos()
            clicker = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.states[self.stateManager.getState()].run(mouse,clicker)

            # print(mouse)
            # print(counter)

            pygame.display.update()
            self.clock.tick(FPS)

class scene1:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        global decoded_text
        self.display.blit(mainMenu,(0,0))
        ret, frame = cap.read()
        if not ret:
            print("No frames Returned")
        


        cropped = frame[160:240, 320:400]
        resized = cv.resize(cropped,(300,300))
        resized = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
        cv.rectangle(frame,(240,160),(400,320),(0,0,255),1)
        cropped = cv.rotate(cropped, cv.ROTATE_90_COUNTERCLOCKWISE)
        cropped = cv.resize(cropped,(300,300))
        pyFrame = pygame.surfarray.make_surface(cropped)
        ref1= resized[42,42]
        ref4= resized[42, 70]
        self.display.blit(pyFrame,(560,150))

        if int(ref1) <= 100 and int(ref4) >= 150:
            try: 
                cv.imwrite('qrRead.jpg', frame)
                decoded_text = QReader().detect_and_decode(image=frame)
                print(decoded_text[0])
                qrTicket = qrFont.render(decoded_text[0], 0, Green)
                self.display.blit(qrTicket, (425,485, 100, 50))
                self.stateManager.setState('scene2')
            except:
                print("error in qr")

        else:
            noQR = dfont.render("No QR Detected", 0, Red)
            self.display.blit(noQR, (480,480, 100, 50))
        


class scene2:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager
        self.clock = pygame.time.Clock()

    def run(self, mouse, clicker):
        self.display.blit(ticketScanned,(0,0))

        try:
            ticketValue = decoded_text[0]
            ref = db.reference(f"/transaction/{ticketValue}")
            print(f"this is the path: /transaction/{ticketValue}")
            #ref.child("name").get()
            transactionStatus = ref.child("status").get()

            if transactionStatus == "pending":
                ref.update({"status":"printing"})
                transactionType = ref.child("transactionType").get()
                if transactionType == "printing":
                    print("For printing")

                    global printParams

                    printParams = [ref.child("colortype").get(),
                                   ref.child("papersize").get(),
                                   ref.child("paymenttype").get(),
                                   ref.child("totalPages").get(),
                                   ref.child("totalPrice").get(),
                                   ref.child("name").get(),
                                   ref.child("url").get()]
                    
                    if printParams[2] == "OnlinePayment":
                        print("online!")
                        self.stateManager.setState('scene3')
                    
                    

                elif transactionType == "top-up":
                    print("For Top up")
                    self.stateManager.setState('scene7')
                else:
                    print("invalid Code")

            else:
                print("No transaction Type")
                print(ref.child("transactionStatus").get())
                self.stateManager.setState('scene1')

        except Exception as error:
            print("INVALID TICKET")
            print(error)
            self.stateManager.setState('scene1')


        

class scene3:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        self.display.blit(nowPrinting,(0,0)) 

        if printParams[1] == "Short" and printParams[0] == "BnW":
            print("short and BnW!")
            GPIO.output(relIn3, GPIO.LOW)

            printerName = "shortBond_Gray"
            
            fileName = printParams[5]

            os.system(f"wget -O {fileName} {printParams[6]}")

            if GPIO.input(limSwB) == 0:
                pwmA.ChangeDutyCycle(45)
                pwmB.ChangeDutyCycle(45)
                GPIO.output(motInA, GPIO.LOW)
                GPIO.output(motInB, GPIO.HIGH)

                GPIO.output(servoButA, GPIO.LOW)
                GPIO.output(servoButB, GPIO.HIGH)
            else:
                GPIO.output(motInA, GPIO.LOW)
                GPIO.output(motInB, GPIO.LOW)
                shortDispenser(int(printParams[3]))
                time.sleep(3)
                GPIO.output(relIn3, GPIO.HIGH)
                # os.system(f"lp -d {printerName} {fileName}")
                
                print("printing...")
                printParams[1] = "dataCleared"

        elif printParams[1] == "Short" and printParams[0] == "Colored":

            print("short and Colored!")
            GPIO.output(relIn3, GPIO.LOW)

            printerName = "shortBond_Colored"
            
            fileName = printParams[5]

            os.system(f"wget -O {fileName} {printParams[6]}")

            if GPIO.input(limSwB) == 0:
                pwmA.ChangeDutyCycle(45)
                pwmB.ChangeDutyCycle(45)
                GPIO.output(motInA, GPIO.LOW)
                GPIO.output(motInB, GPIO.HIGH)

                GPIO.output(servoButA, GPIO.LOW)
                GPIO.output(servoButB, GPIO.HIGH)
            else:
                GPIO.output(motInA, GPIO.LOW)
                GPIO.output(motInB, GPIO.LOW)
                shortDispenser(int(printParams[3]))
                time.sleep(3)
                GPIO.output(relIn3, GPIO.HIGH)
                # os.system(f"lp -d {printerName} {fileName}")

                print("printing...")
                printParams[1] = "dataCleared"

        else:
            print("Printing done!")
            self.stateManager.setState('scene1')
            
class scene4:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        self.display.blit(getDocuPrompt,(0,0))

class scene5:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        self.display.blit(onHoldCoin,(0,0))

class scene6:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        self.display.blit(onHoldTap,(0,0))        
        
class scene7:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):

        GPIO.output(servoButB, GPIO.HIGH)
        GPIO.output(servoButA, GPIO.LOW)
        GPIO.output(extraButC, GPIO.HIGH)

        self.display.blit(topUpMode,(0,0))

        coinVal = ser.read(2)
        coinRead = coinVal.decode("utf-8")
        print(coinRead)
        coinValText = topUpFont.render(f"{coinRead}", 0, Red)
        self.display.blit(coinValText, (690,250))
    
        timer = topUpFont.render("10", 0, Red)
        self.display.blit(timer, (580,490))
class scene8:
    def __init__(self, display, stateManager):
        self.display = display
        self.stateManager = stateManager

    def run(self, mouse, clicker):
        self.display.blit(topUpSuccess,(0,0))


class stateManager:
    def __init__(self, currentScene):
        self.currentScene = currentScene
    
    def getState(self):
        return self.currentScene
    
    def setState(self, state):
        self.currentScene = state

if __name__ == '__main__':
    game = Game()
    game.run()