import imagezmq
import socket
import time
import cv2

sender = imagezmq.ImageSender(connect_to="tcp://68.183.80.245:5555")

cap = cv2.VideoCapture("output2.avi")

rpiName = socket.gethostname()
print(rpiName)

while True:
    ret, frame = cap.read()
    # Serialize frame

    msg = sender.send_image(rpiName, frame)
    print(msg)
