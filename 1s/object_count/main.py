import zmq
import cv2
import numpy as np
from skimage.filters import threshold_otsu, sobel

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port=5555

socket.connect("tcp://192.168.0.100:%s" % port)
cv2.namedWindow("Client recv", cv2.WINDOW_GUI_NORMAL)
count = 0
while True:
    msg = socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    # hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #
    # pixel = frame[1, 1]
    # back = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]
    #
    # lower_bound = (back[0]-30, back[1]-30, back[2]-30)
    # upper_bound = (back[0]+30, back[1]+30, back[2]+30)
    #
    # mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    #
    # result = cv2.bitwise_and(frame, frame, mask=mask)
    #
    #

    count += 1
    key = cv2.waitKey(100)
    if key == ord('q'):
        break
    cv2.putText(frame, f"Count {count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0))
    cv2.imshow("Client recv", frame)