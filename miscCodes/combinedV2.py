import numpy as np 
import cv2 as cv
import torch
import time
import os
import easyocr
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import mysql.connector

db = mysql.connector.connect(
    
    host = "localhost",
    user = "root",
    passwd = "",
    database = "testdatabase"

)

        # myCursor.execute("INSERT INTO truckban (truckImageID, truckPlateID, truckPlateString) VALUES (%s, %s, %s)", (f"truck{truckImage}.jpg", f"plate{image_number}.jpg", f"plate{image_number}.jpg") )
        # db.commit()

myCursor = db.cursor()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

processPlatesDir = 'tempPlatesDir'
processTrucksDir = 'tempTrucksDir'

plateModel = torch.hub.load('yolov5','custom', source= 'local', path = 'plate_number.pt', force_reload=True)
reader = easyocr.Reader(['en'])

images_directory = 'truckImages'  # Replace with the path to your images directory
output_directory_plates = 'plateImages'
image_number = 0


currentID = 1
output_directory = 'truckImages'
truckImage = 0

winX, winY = 1366, 768

lineParam = 1000

vidX, vidY = 3840, 2160

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = torch.hub.load('yolov5', 'custom', source='local', path='truck_v6.pt', force_reload=True)
cap = cv.VideoCapture('videos\Truck3.avi')

print("Using Device", device)

trucks = []
plates = []
plateStrings = []


def runOCR():
    print("Running OCR...")
    global image_number

    for image_file in os.listdir(processTrucksDir):
        if image_file.endswith('.jpg') or image_file.endswith('.png'):  # Check for image files
            image_path = os.path.join(processTrucksDir, image_file)
            frame = cv.imread(image_path)
            frame = cv.resize(frame, (640, 640))

            result = plateModel(frame)
            result_df = result.pandas().xyxy[0]

            # result = reader.readtext(truck_frame, detail=0)
            for ind in result_df.index:
                x1, y1 = int(result_df['xmin'][ind]), int(result_df['ymin'][ind])
                x2, y2 = int(result_df['xmax'][ind]), int(result_df['ymax'][ind])

                label = result_df['name'][ind]
                conf = result_df['confidence'][ind]

                if conf >= 0.85:
                    text = label + ' ' + str(conf.round(decimals=2))
                    cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv.putText(frame, text, (x1, y1 - 5), cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                    crops = frame[x1:y1, x2:y2]

                    cropped_img = frame[int(y1):int(y2), int(x1):int(x2)]
                    ####adjust plate number size and quality
                    scale = 6  # Adjust this value to control the level of de-pixelation
                    # Resize the image using bilinear interpolation
                    height, width, _ = cropped_img.shape
                    new_height = scale * height
                    new_width = scale * width
                    resized_image = cv.resize(cropped_img, (new_width, new_height), interpolation=cv.INTER_LINEAR)
                    # Convert the image to grayscale
                    gray_image = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)
                    # Apply Gaussian blur to the image
                    # sharpened_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 8)
                    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                    sharpened_image = cv.filter2D(gray_image, -1, kernel)

                    # write in directory
                    cv.imwrite(os.path.join(output_directory_plates, f"plate{image_number}.jpg"), sharpened_image)
                    cv.imwrite(os.path.join(processPlatesDir, "tempPlates"), sharpened_image)
                    plates.append(sharpened_image)
                    # convert image to text
                    plate_result = reader.readtext(sharpened_image, detail=0)
                    text = tess.image_to_string(sharpened_image)

                    if len(plate_result) == 1:
                        finalPlate = plate_result[0]
                    elif len(plate_result) == 2:
                        finalPlate = plate_result[0] + plate_result[1]
                    else:
                        finalPlate = "{Null Plate}"

                    #commit to database
                    myCursor.execute("INSERT INTO truckban (truckImageID, truckPlateID, truckPlateString) VALUES (%s, %s, %s)", (f"truck{truckImage}.jpg", f"plate{image_number}.jpg", finalPlate) )
                    db.commit()

                    image_number += 1
                    # Display the results
                    print(text + " -- " + str(plate_result))
                    print(finalPlate)
                    try:
                        os.remove('tempTrucksDir/tempTruck.jpg')
                    except:
                        print("no Image in temTrucks")

    

    


                        




def class_to_label(x):
    return model.names[int(x)]


def plot_boxes(results, frame, height, width, confidence=0.90):
    labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    detections = []

    n = len(labels)
    x_shape, y_shape = width, height

    for i in range(n):
        row = cord[i]

        if row[4] >= confidence:
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)

            if class_to_label(labels[i]) == 'truck':
                x_center = x1 + (x2 - x1)
                y_center = y1 + ((y2 - y1) / 2)

                tlwh = np.asarray([x1, y1, int(y2 - y1)], dtype=np.float32)
                confidence = float(row[4].item())
                feature = 'truck'

                detections.append(([x1, y1, int(x2 - x1), int(y2 - y1)], row[4].item(), 'truck'))

    return frame, detections


from deep_sort_realtime.deepsort_tracker import DeepSort

object_tracker = DeepSort(max_age=5,
                          n_init=2,
                          nms_max_overlap=1.0,
                          max_cosine_distance=0.3,
                          nn_budget=None,
                          override_track_class=None,
                          embedder="mobilenet",
                          half=True,
                          bgr=True,
                          embedder_gpu=True,
                          embedder_model_name=None,
                          embedder_wts=None,
                          polygon=False,
                          today=None)

currVal = [0]

while cap.isOpened():
    succes, img = cap.read()
    start = time.perf_counter()

    results = model(img)
    img, detections = plot_boxes(results, img, height=img.shape[0], width=img.shape[1], confidence=0.90)

    tracks = object_tracker.update_tracks(detections, frame=img)

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id

        ltrb = track.to_ltrb()
        bbox = ltrb

        if int(bbox[3]) > vidY - lineParam:
            currVal.append(track_id)

        if len(currVal) == 5:
            currVal.pop(0)

        cState = currVal[len(currVal) - 1]
        lState = currVal[len(currVal) - 2]

        cv.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 0, 255), 2)
        cv.putText(img, "ID: " + str(track_id), (int(bbox[0]), int(bbox[1] - 10)), cv.FONT_HERSHEY_SIMPLEX, 1.5,
                   (0, 255, 0), 2)

        #print(int(bbox[3]))
        #print(f"Line value: {vidY - lineParam}")

        if cState != lState:
            print(f"Captured saved as: {truckImage}")
            cropped_img = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
            cv.imwrite(os.path.join(output_directory, f"truck{truckImage}.jpg"), cropped_img)
            cv.imwrite(os.path.join(processTrucksDir, "tempTruck.jpg"), cropped_img)
            runOCR()
            truckImage += 1
            trucks.append(truckImage)

    # print(currVal)

    end = time.perf_counter()
    totalTime = end - start
    fps = 1 / totalTime

    cv.putText(img, f'FPS: ({int(fps)})', (20, 70), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    cv.line(img, (0, vidY - lineParam), (vidX, vidY - lineParam), (0, 0, 255), 2)
    img = cv.resize(img, (winX, winY))
    # cv.line(img, (0, winY-lineParam), (winX, winY-lineParam), (0, 255, 0), 2)
    cv.imshow('TruckBan', img)

    # myCursor.execute("INSERT INTO truckban (truckImageID, truckPlateID, truckPlateString) VALUES (%s, %s, %s)", (f"truck{truckImage}.jpg", f"plate{image_number}.jpg", f"plate{image_number}.jpg") )
    # db.commit()



    # print("Truck list:", trucks)
    # print("Plates list", plates)
    # print("String", plateStrings)
    # print(len(trucks), len(plates), len(plateStrings))

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()