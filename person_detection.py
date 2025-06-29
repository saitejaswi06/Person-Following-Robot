import cv2
import json
import socket
import signal
import sys
from simple_pid import PID
import torch

# Load YOLOv5 model from Ultralytics
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  

# Used to communicate with the NodeMCU
ESP_IP = "ESP IP ADDRESS"  # CHANGE IP 1 address of the NodeMCU
ESP_PORT = 80            # OPTIONAL CHANGE 2 Port number of the socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ESP_IP, ESP_PORT))   
print(f"Connected to ESP at {ESP_IP}:{ESP_PORT}")   

# Use webcam for video capture
# Set video resolution as 640x360, Quality 20 and FPS 5 in IP Webcam
VIDSTREAM = "IPv4 from IPWebcam + /video"

# Initialize PID controller
pid = PID(0, 0, 0, setpoint=0)

# Initialize dictionary for sending data over the network
param_dict = {
    "pwmR": 0, 
    "pwmL": 0, 
}

color = (255, 255, 255)

pwm = 0

# Slider functions for PID tuning
def slider_kp(val):
    pid.Kp = round(val * 0.1, 3)

def slider_ki(val):
    pid.Ki = round(val * 0.01, 3)

def slider_kd(val):
    pid.Kd = round(val * 0.1, 3)


# Helper function to 1. Encode the dictionary to json and then to bytes 2. Send the bytes over the TCP socket. 
def send_over_socket(param_dict): 
    json_data = json.dumps(param_dict) + '\n'
    encoded_data = json_data.encode()
    client_socket.sendall(encoded_data)
    print(f"Sent: {json_data.strip()}")

# Signal handler to ensure clean exit of the program  
def signal_handler(signal, frame):
    send_over_socket({"pwmR": 0, "pwmL": 0})
    sys.exit(0)

# Create a window with trackbars for PID tuning
Winname = 'PID Slider'
signal.signal(signal.SIGINT, signal_handler) # SIGINT is the signal sent by the OS when you press Ctrl+C. 
cv2.namedWindow(Winname)
cv2.createTrackbar('Kp', Winname, 0, 100, slider_kp)
cv2.createTrackbar('Ki', Winname, 0, 100, slider_ki)
cv2.createTrackbar('Kd', Winname, 0, 100, slider_kd)

# Open video stream
cap = cv2.VideoCapture(VIDSTREAM)

# If there is video available
if cap.isOpened():
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    pid.setpoint = width // 2 # Set the setpoint to the center of the frame
    pid.output_limits = (-250, 250)
    print(width, height, sep=",")


while cap.isOpened():
    success , frame = cap.read() # Get the video frame
    if not success:
        continue

    # YOLOv5 inference
    results = model(frame)

    # Process results
    # results.xyxyn => [[ [x1, y1, x2, y2, conf, class] , [x1, y1, x2, y2, conf, class] , ...], ...]
    labels, coords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    

    for i in range(len(labels)):
        if labels[i] == 0:  # Class ID for person
            x1, y1, x2, y2, conf = coords[i] # x1, y1, x2, y2 are the coordinates of the bounding box. conf is the confidence of the detection
            x1, y1, x2, y2 = int(x1 * width), int(y1 * height), int(x2 * width), int(y2 * height)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 5, color, -1)
            cv2.putText(frame, f"Person ({conf})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # If in center, charge forward
            if (width//2)-50 < cx < (width//2)+50:
                param_dict["pwmL"] = param_dict["pwmR"] = 255
                
            else:
                pwm = int(pid(cx))
                param_dict["pwmL"] = -pwm
                param_dict["pwmR"] = pwm

            # Since motor won't work for low pwm, we need to add a threshold
            threshold = 150
            if pwm > 0:
                pwm += threshold
            else: 
                pwm -= threshold

            break

    else:
        # If nothing is detected
        param_dict["pwmL"] = 0
        param_dict["pwmR"] = 0

    send_over_socket(param_dict)

    # Display the frame
    cv2.putText(frame, f"Kp: {pid.Kp}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)
    cv2.putText(frame, f"Ki: {pid.Ki}", (10, 60), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)
    cv2.putText(frame, f"Kd: {pid.Kd}", (10, 90), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)

    cv2.imshow("Frame", frame)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break


# For clean exit
param_dict["pwmL"] = 0
param_dict["pwmR"] = 0

client_socket.close()
cap.release()
cv2.destroyAllWindows()
