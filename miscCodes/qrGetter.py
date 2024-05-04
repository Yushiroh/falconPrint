import cv2 as cv
import torch
from PIL import Image
import time
from qreader import QReader

# model = torch.hub.load('ultralytics/yolov5', 'custom', path='qr100Epochs.pt', force_reload= False)

# img = cv2.imread('sample0.jpg') 
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("No cam detected")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("No frames Returned") 
        break
    
    # frame = cv.resize(frame, (200,200))
    cropped = frame[160:240, 320:400]
    resized = cv.resize(cropped,(300,300))
    resized = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
    cv.rectangle(frame,(240,160),(400,320),(0,0,255),1)
    cv.imshow('frame', frame)
    ref1= resized[42,42]
    ref4= resized[42, 70]
    print(f"ref1 = {ref1} and ref 4 is = {ref4}")
    if int(ref1) <= 100 and int(ref4) >= 150:
        print("QR YARN!")
        decoded_text = QReader().detect_and_decode(image=frame)
        print(decoded_text)

    # try:
    #     results = model(frame, size=640)  
    #     pandaData = results.pandas().xyxy[0]
    #     detectName = pandaData.iloc[0]['name']
    #     confidenceFrame = pandaData.iloc[0]['confidence']
    #     if confidenceFrame >= 0.95:
    #         decoded_text = QReader().detect_and_decode(image=frame)
    #         print(detectName)
    #         print(decoded_text)

    # except:
    #     print("No detection!")
   
    if cv.waitKey(1) == ord('q'):
        break