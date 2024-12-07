import cv2
import time
from contourpy.util.data import simple
from fontTools.misc.cython import returns
from networkx import tree_graph

winname_camera = "Camera"
winname_mask = "Mask"
cv2.namedWindow(winname_camera, cv2.WINDOW_NORMAL)
cv2.namedWindow(winname_mask, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

# 20-30, 220-255, 60-120
lower = (150, 100, 50)
upper = (190, 200, 300)

D = 0.077
prev_time = time.time()
curr_time = time.time()
r = 1

trajectory = []
l = 15

while camera.isOpened():
    ret, frame = camera.read()
    curr_time = time.time()
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        x, y = int(x), int(y)

        trajectory.append((x, y))
        if len(trajectory) > l:
            trajectory.pop(0)

        if r>10:
            cv2.circle(frame, (int(x), int(y)), 5, (0,0,255), -2)
            cv2.circle(frame, (int(x), int(y)), int(r), (0,0,255), 2)

        for i in range(1, len(trajectory)):
            cv2.line(frame, trajectory[i], trajectory[i-1], (255 * (i / len(trajectory)),0,0), i)

        time_dif = curr_time - prev_time
        if len(trajectory) > 1:
            p1 = trajectory[-1]
            p2 = trajectory[-2]
            dx = p1[0] - p2[0]
            dy = p1[1] - p2[1]
            dist =  (dx ** 2 + dy ** 2) ** 0.5
            pxl_per_metr = D / (r * 2)
            dist *= pxl_per_metr
            speed  = dist / time_dif

            cv2.putText(frame, f"Speed = {speed:.3f}", (10,60), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255,255,0))
    else:
        trajectory = []

    prev_time = curr_time

    cv2.imshow(winname_mask, mask)
    cv2.imshow(winname_camera, frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()