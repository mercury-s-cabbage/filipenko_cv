import numpy as np
import cv2

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

camera = cv2.VideoCapture(0)

roi = None
while camera.isOpened():
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if roi is not None:
        corr_image = cv2.matchTemplate(gray, roi, cv2.TM_CCORR_NORMED)
        #cv2.imshow("Corr", corr_image)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(corr_image)
        top_left = max_loc
        bottom_right = (top_left[0] + roi.shape[1], top_left[1] + roi.shape[0])
        cv2.rectangle(frame, top_left, bottom_right, (255, 0, 255), 2)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    if key == ord('s'):
        result = cv2.selectROI("ROI SELECTION", gray)
        roi = gray[int(result[1]):int(result[1] + result[3]), int(result[0]) : int(result[0] + result[2])]

        cv2.imshow("ROI", roi)
        cv2.destroyWindow("ROI SELECTION")

camera.release()
cv2.destroyAllWindows()