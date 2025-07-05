# 🚶 Person-Following Differential Drive Robot | OpenCV + ESP8266

> A real-time person-tracking robot leveraging computer vision for object/person detection and autonomous motion control, implemented on a differential-drive platform powered by ESP8266 and L293D motor driver.

---

## 🎯 Objective

Build a **vision-guided mobile robot** capable of tracking and following a person based on color/shape detection, enabling contactless human-following behavior for applications like personal assistants, warehouse bots, and surveillance platforms.

---

## ⚙️ Technologies Used

| Domain                  | Tools / Libraries                           |
|--------------------------|---------------------------------------------|
| Person Detection         | OpenCV (Haar Cascades / Color Segmentation) |
| Image Processing         | OpenCV, NumPy                               |
| Object Tracking          | Centroid Tracking / Contour Detection       |
| Robot Control            | ESP8266, Embedded C, WiFi/Serial Protocol  |
| Motor Driver             | L293D                                       |
| Embedded Communication   | UART / Wi-Fi (HTTP / TCP)                  |
| Platform                 | Raspberry Pi / PC (Vision), ESP8266 (Control) |

---

## 🔩 Hardware Stack

| Module               | Purpose                          |
|----------------------|----------------------------------|
| ESP8266 NodeMCU       | Wi-Fi-enabled robot controller   |
| L293D Motor Driver    | Controls 2 DC motors             |
| Differential Drive    | Robot chassis (Left & Right)    |
| USB / Pi Camera       | Captures live video feed        |
| Power Supply          | 9V Battery + 7805 Regulator     |

---

## 🛠️ Implementation Steps

### ➤ Vision & Detection Pipeline
- Used OpenCV for:
   - **Color thresholding:** Person wearing a distinct-colored shirt.
   - **Contour detection:** Calculated bounding boxes and centroids.
   - **Distance estimation:** Used bounding box size as a proxy for distance.
- Optional: Used Haar cascade classifiers or HOG + SVM person detection.

### ➤ Tracking & Command Generation
- Tracked the person's centroid relative to the camera frame center.
- Generated commands (`FORWARD`, `BACKWARD`, `LEFT`, `RIGHT`, `STOP`) based on horizontal & distance offset.

### ➤ Robot Control
- Sent commands to ESP8266 over:
   - Serial UART **OR**
   - Wi-Fi (TCP sockets / HTTP requests).
- ESP8266 drove the **L293D motor driver** to move towards the person.

---

## 🔬 Key Features

- Person following based on color or shape, with real-time decision-making.
- Adjustable tracking sensitivity and speed control.
- Supports remote camera module (e.g., on Raspberry Pi) for distributed systems.

---

## 📈 Improvements & Future Scope

- Integrate **YOLOv8** or TensorFlow Lite for person detection on edge devices.
- Add ultrasonic sensors for obstacle detection during tracking.
- Implement Kalman Filters or Optical Flow for smoother tracking.
- Move to a Jetson Nano or Raspberry Pi 4 for complete onboard processing.

---

## 🛡️ Summary

This project demonstrates a **vision-powered autonomous robot** for dynamic person tracking using lightweight computer vision algorithms and a microcontroller-based drive system. It bridges real-time perception with embedded control for autonomous navigation.

---
