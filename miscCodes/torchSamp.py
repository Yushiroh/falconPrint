import cv2 as cv
import torch
from PIL import Image
from qreader import QReader

model = torch.hub.load('ultralytics/yolov5', 'custom', path='qr100Epochs.pt', force_reload= False)

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

    cv.imshow('frame', frame)

    try:
        results = model(frame, size=640)  
        pandaData = results.pandas().xyxy[0]
        detectName = pandaData.iloc[0]['name']
        confidenceFrame = pandaData.iloc[0]['confidence']
        if confidenceFrame >= 0.95:
            decoded_text = QReader().detect_and_decode(image=frame)
            print(detectName)
            print(decoded_text)

    except:
        print("No detection!")
   
    if cv.waitKey(1) == ord('q'):
        break