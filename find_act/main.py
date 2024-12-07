import numpy as np
import cv2

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.namedWindow("Background", cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

background = None
prev_frame = None
while camera.isOpened():
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if background is not None:
        delta = cv2.absdiff(background, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if prev_frame is not None:
            diff = cv2.absdiff(thresh, prev_frame)
            changes = diff.sum() / 255 / diff.size
            if changes / diff.size < 0.05:
                background = gray.copy()
        prev_frame = thresh

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.imshow("Background", thresh)


    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('b'):
        background = gray.copy()
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()