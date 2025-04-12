import cv2 as cv
import time
import serial
import os
import csv
import requests

# Set up serial communication with Arduino
arduino = serial.Serial(port='COM9', baudrate=9600, timeout=1)  # Change COM3 to your Arduino's port

# Reading label names from obj.names file
class_name = []
with open(os.path.join("project_files", 'obj.names'), 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

# Importing model weights and config file
net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
net1.setPreferableBackend(cv.dnn.DNN_BACKEND_DEFAULT)
net1.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

model1 = cv.dnn_DetectionModel(net1)
model1.setInputParams(size=(640, 480), scale=1/255, swapRB=True)


# Define the video source (0 for the default camera)
cap = cv.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))

# Check if the webcam is opened correctly
if not cap.isOpened() or width == 0 or height == 0:
    print("Error: Unable to access the webcam.")
    exit()

# Path for storing result files
result_path = "pothole_coordinates"
if not os.path.exists(result_path):
    os.makedirs(result_path)

# Log file path for CSV
log_file_path = "pothole_detection_log.csv"

# Initialize CSV with header if file doesn't exist
if not os.path.exists(log_file_path):
    with open(log_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Serial No.', 'Date of Detection', 'Location Name', 'Latitude', 'Longitude', 'Threat Level', 'Pothole Status'])

starting_time = time.time()
Conf_threshold = 0.5
NMS_threshold = 0.4
frame_counter = 0
i = 0
b = 0
serial_no = 1

# Function to send data to Arduino via serial
def send_to_arduino(message):
    arduino.write(message.encode())  # Send message to Arduino

# Helper function for reverse geocoding using Nominatim (OpenStreetMap)
def get_location_name_nominatim(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            data = response.json()
            if 'address' in data:
                address = data['address'].get('road', 'Unknown')
                return address
            else:
                return 'Unknown'
        else:
            return 'Unknown'
    except Exception as e:
        print(f"Error fetching location: {e}")
        return 'Unknown'

# Detection loop
while True:
    ret, frame = cap.read()
    frame_counter += 1
    if not ret:
        break

    # Analyze the stream with detection model
    classes, scores, boxes = model1.detect(frame, Conf_threshold, NMS_threshold)
    
    for (classid, score, box) in zip(classes, scores, boxes):
        label = "pothole"
        x, y, w, h = box
        recarea = w * h
        area = width * height

        # Calculate threat level based on confidence score
        if len(scores) != 0 and scores[0] >= 0.7:
            threat_level = "SEVERE"
            threat_color = (0, 0, 255)  # Red for severe
        elif len(scores) != 0 and scores[0] >= 0.5:
            threat_level = "INTERMEDIATE"
            threat_color = (0, 255, 255)  # Yellow for intermediate
        else:
            threat_level = "DETECTED"
            threat_color = (0, 255, 0)  # Green for detected but less confident

        if (recarea / area) <= 0.1 and box[1] < 600:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv.putText(frame, f"{round(scores[0] * 100, 2)}% {label}", (box[0], box[1] - 10), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
            cv.putText(frame, f"Threat: {threat_level}", (x, y + h + 20), cv.FONT_HERSHEY_COMPLEX, 0.7, threat_color, 2)

            if i == 0:
                cv.imwrite(os.path.join(result_path, f'pothole{i}.jpg'), frame)
                i += 1

            if i != 0 and (time.time() - b) >= 2:
                # Manually set latitude and longitude
                lat = 11.726145  # Replace with your manual latitude
                lon = 75.540045  # Replace with your manual longitude

                # Get the location name from geolocation
                location_name = get_location_name_nominatim(lat, lon)

                # Prepare message to send to Arduino (latitude, longitude, threat level, and pothole status)
                message = f"LAT: {lat}, LON: {lon}, THREAT: {threat_level}, STATUS: {threat_level}\n"
                send_to_arduino(message)  # Send to Arduino via serial

                # Log the detection to CSV
                with open(log_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([serial_no, time.ctime(time.time()), location_name, lat, lon, threat_level, threat_level])
                serial_no += 1

                b = time.time()
                i += 1

    # Writing FPS on frame
    ending_time = time.time() - starting_time
    fps = frame_counter / ending_time
    cv.putText(frame, f'FPS: {fps:.2f}', (20, 50), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    # Showing the frame
    cv.imshow('Live Detection', frame)

    # Exit on pressing 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# End the video capture
cap.release()
cv.destroyAllWindows()
