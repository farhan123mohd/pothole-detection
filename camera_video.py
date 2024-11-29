import cv2 as cv

import time

import os



# Read label names from obj.names file

class_name = []

with open(os.path.join("project_files", 'obj.names'), 'r') as f:

    class_name = [cname.strip() for cname in f.readlines()]



# Load YOLOv4 Tiny model

net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')

net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)

net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)  # Use CUDA FP16 for speed

model1 = cv.dnn_DetectionModel(net1)

model1.setInputParams(size=(416, 416), scale=1/255, swapRB=True)  # Use 416x416 for faster processing



# Initialize webcam

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)   # Set low resolution for speed

cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

cap.set(cv.CAP_PROP_FPS, 60)           # Request a higher frame rate from the camera



# Check if the webcam is opened correctly

if not cap.isOpened():

    print("Error: Unable to access the webcam.")

    exit()



# Start detection

frame_counter = 0

starting_time = time.time()



while True:

    ret, frame = cap.read()

    if not ret:

        break



    frame_counter += 1



    # Downscale the frame for processing

    resized_frame = cv.resize(frame, (416, 416))  # YOLOv4-Tiny input size



    # Run detection

    classes, scores, boxes = model1.detect(resized_frame, confThreshold=0.5, nmsThreshold=0.4)



    # Draw boxes (optional: comment this out for even higher FPS)

    for (classid, score, box) in zip(classes, scores, boxes):

        label = f"{class_name[classid[0]]}: {round(score[0] * 100, 2)}%"

        x, y, w, h = box

        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv.putText(frame, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)



    # Calculate and display FPS

    elapsed_time = time.time() - starting_time

    fps = frame_counter / elapsed_time

    cv.putText(frame, f"FPS: {fps:.2f}", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)



    # Show the frame

    cv.imshow("Pothole Detection", frame)



    # Exit on 'q'

    if cv.waitKey(1) & 0xFF == ord('q'):

        break



# Release resources

cap.release()

cv.destroyAllWindows()

