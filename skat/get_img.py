from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import cv2

winnameOrigin = "Image Origin"
cv2.namedWindow(winnameOrigin, cv2.WINDOW_NORMAL)
winnameGray = "Image Gray"
cv2.namedWindow(winnameGray, cv2.WINDOW_NORMAL)

vcap = cv2.VideoCapture("rtsp://192.168.43.1:8080/h264_ulaw.sdp")

dest_pts = np.float32([[750,135],[1110,150], [1100,685], [705,675]])
rect_width = 400
rect_height = 600
src_pts = np.float32([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]])

M = cv2.getPerspectiveTransform(dest_pts, src_pts)

if not vcap.isOpened():
    print("Error: Cannot open RTSP stream.")
    exit()

while True:
    ret, frame = vcap.read()
    cv2.imshow(winnameOrigin, frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]
    thresh = cv2.dilate(thresh, None, iterations=5)


    warped = cv2.warpPerspective(thresh, M, (rect_width, rect_height))

    cv2.imshow(winnameGray, warped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vcap.release()
cv2.destroyAllWindows()
