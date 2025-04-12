
# 🚧 Real-Time Pothole Detection using YOLOv4-Tiny & OpenCV 🚗

Detect potholes from **real-time video stream or images** using Python. Also prints GPS location (latitude & longitude) and logs all detections into a `.csv` (Excel-readable) file.

> ⚠️ Need help? Feel free to open an issue on the [GitHub repository](https://github.com/farhan123mohd/pothole-detection/issues).

---

## 🔧 Technologies Used

- ⚙️ YOLOv4-Tiny
- 🎥 OpenCV
- 🐍 Python
- 🌍 Geolocation API (OpenStreetMap)
- 📄 CSV Logging

---

## 🛠️ Setup Instructions

### 📁 1. Clone the repository
```bash
git clone https://github.com/farhan123mohd/pothole-detection.git
cd pothole-detection
```

### ⬆️ 2. Upgrade pip
```bash
pip install --upgrade pip
```

### 📦 3. Install required packages
```bash
pip install opencv-python
pip install geocoder
pip install pyserial
```

### ▶️ 4. Run the application
```bash
python camera_video.py
```

---

## ✨ Features

✅ Real-time pothole detection using live webcam  
✅ Detection using YOLOv4-Tiny (lightweight & fast)  
✅ Annotated video frames with bounding boxes  
✅ Logs latitude, longitude, location name, threat level  
✅ CSV output for data analysis/reporting

---

## 📍 Output Example

### 🖼️ Image Output

![Example Results](https://github.com/noorkhokhar99/pothole-detection/blob/main/result1.jpg)

### 📄 CSV Log Output
```
Serial No. | Date of Detection | Location Name | Latitude   | Longitude  | Threat Level | Pothole Status
-----------------------------------------------------------------------------------------------
1          | Tue Apr 02 12:34  | Main St       | 11.726145  | 75.540045  | SEVERE       | SEVERE
```

---

## 🚀 Coming Soon

- 🗺️ Live map visualization of detected potholes
- 📱 Mobile app support
- ☁️ Cloud-based storage/database integration

---

## 🤝 Support

If you face any issues or want to contribute:
- Open an [Issue](https://github.com/farhan123mohd/pothole-detection/issues)
- Contact +91 8848523864
- Submit a Pull Request

---

## 🧠 Credits

Made with ❤️ using Python, YOLOv4-Tiny, and OpenCV.


