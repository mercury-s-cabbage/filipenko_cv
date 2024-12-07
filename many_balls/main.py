import numpy as np
import cv2
import random
import time

diff = 30
diff2 = 50
g = [72, 149, 169]
y = [28, 111, 206]
r = [172, 212, 176]
b = [98, 237, 173]
colors = ["red", "green", "yellow", "blue"]
winname_camera = "Camera"
winname_mask = "Mask"

r_lower = (r[0] - diff, r[1] - diff2, r[2] - diff2)
r_upper = (r[0] + diff, r[1] + diff2, r[2] + diff2)
y_lower = (y[0] - diff, y[1] - diff2, y[2] - diff2)
y_upper = (y[0] + diff, y[1] + diff2, y[2] + diff2)
g_lower = (g[0] - diff, g[1] - diff2, g[2] - diff2)
g_upper = (g[0] + diff, g[1] + diff2, g[2] + diff2)
b_lower = (b[0] - diff, b[1] - diff2, b[2] - diff2)
b_upper = (b[0] + diff, b[1] + diff2, b[2] + diff2)

random.shuffle(colors)

def guess(image, colors):
    return False

def find(lower, upper, color):
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        x, y = int(x), int(y)


        if r>10:
            cv2.circle(frame, (int(x), int(y)), 5, upper, -2)
            cv2.circle(frame, (int(x), int(y)), int(r), color, 2)

        if x is not None:
            return tuple([x, y])

    return tuple([0, 0])


cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
#cv2.namedWindow("Background", cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

answer = ''
while camera.isOpened():
    ret, frame = camera.read()
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    red = find(r_lower, r_upper, tuple(r))
    yellow = find(y_lower, y_upper, tuple(y))
    green = find(g_lower, g_upper, tuple(g))
    blue = find(b_lower, b_upper, tuple(b))

    color_values = {
        "yellow": yellow,
        "red": red,
        "blue": blue,
        "green": green
    }

    sorted_dict = dict(sorted(color_values.items(), key=lambda item: (item[1][1], item[1][0])))
    colors = ["red", "yellow", "green", "blue"]
    if list(sorted_dict.keys()) == colors:
        answer = f"You answer is {sorted_dict.keys()} True"
    else:
        answer = f"You answer is {sorted_dict.keys()} False"
    cv2.putText(frame, answer, (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 0))
    cv2.imshow(winname_camera, frame)

camera.release()
cv2.destroyAllWindows()