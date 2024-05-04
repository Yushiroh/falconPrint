

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os
import cv2 as cv
from qreader import QReader
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

databaseURL = 'https://fileuploading-67153-default-rtdb.asia-southeast1.firebasedatabase.app' 


cred = credentials.Certificate("falconPrint_pKey_fireBase.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':databaseURL
	})

vid = cv.VideoCapture(0)


window = tk.Tk()
window.title('FalconPrint')
window.geometry('700x700')
 
introText = tk.StringVar(value='SCAN TICKET!')
label1 = ttk.Label(window, text='SAMPLE', background='red', textvariable=introText)
label1.pack()






def captureFootage():
    _, frame = vid.read() 
    opencv_image  = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)  
    captured_image = Image.fromarray(opencv_image) 
    photo_image = ImageTk.PhotoImage(image=captured_image) 
    cameraCanvass.photo_image = photo_image 
    cameraCanvass.configure(image=photo_image)
    cameraCanvass.after(5, captureFootage)
    # cameraCanvass.after(10000, qrRead) 



def qrRead():
    _, frame = vid.read() 
    opencv_image  = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)  
    cv.imwrite('sample0.jpg',opencv_image)
    print('ReadingQR')
    qreader = QReader()
    image = cv.cvtColor(cv.imread("sample0.jpg"), cv.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)
    
    try:
        print(decoded_text[0])
        ticketValue = decoded_text[0]
        ref = db.reference(f"/uploadedFiles/{ticketValue[1:21]}")
        print(f"this is the path: /uploadedFiles/{ticketValue[1:21]}")
        print(ref.child("colortype").get())
        print(ref.child("name").get())
        print(ref.child("papersize").get())
        print(ref.child("url").get())
        wgetURL = ref.child("url").get()
        os.system(f'wget -O samplePrint.pdf {wgetURL}')
        time.sleep(10)
        os.system(f'lp -d shortBondTester samplePrint.pdf')

    except:
        print("no qr to read!")

    print("reading done")


    
    

    

cameraCanvass = ttk.Label(window, text='CAM HERE', background='red')
cameraCanvass.pack()

Button1 = ttk.Button(window, text='SAMPLE', command=qrRead)
Button1.pack()

print("running outer")
captureFootage()

window.mainloop()