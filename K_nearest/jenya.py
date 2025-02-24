from time import sleep

import cv2
import numpy as np
import matplotlib.pyplot as plt

winname = "Camera"
cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

haar_cascade = "haarcascades/haarcascade_frontalface_default.xml"
haar_cascade_eyes = "haarcascades/haarcascade_eye_tree_eyeglasses.xml"
face = cv2.CascadeClassifier(haar_cascade)
eyes = cv2.CascadeClassifier(haar_cascade_eyes)
glasses = cv2.imread("dealwithit.png")

def detector(img, classifier, scaleFactor = None, minNeighbors=None):
    result = img.copy()
    rects = classifier.detectMultiScale(result, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

    if len(rects) == 2:
        (x1, y1, w1, h1) = rects[0]
        (x2, y2, w2, h2) = rects[1]
        return (x1, y1, abs(x1-x2)+w2, abs(y1-y2)+h2)
    return None


while camera.isOpened():
    ret, frame = camera.read()
    d = detector(frame, eyes, 1.2, 5)
    # if we get 2 eyes
    if d:
        (x, y, w, h) = d
        x = int(x * 0.9)
        y = int(y * 0.9)

        w = int(w * 2)
        h = int(h * 2)

        glasses_new = cv2.resize(glasses, dsize=(w, h), fx=2, fy=2)
        glasses_new = np.where(glasses_new[0: h, 0: w if x+w < frame.shape[1] else frame.shape[1] - x,] == 0,
                               glasses_new[0: h if y+h < frame.shape[0] else frame.shape[0] - y, 0: w if x+w < frame.shape[1] else frame.shape[1] - x,],
                               frame[y:min(y+h, frame.shape[0]), x:min(x+w, frame.shape[1])])

        frame[y:min(y+h, frame.shape[0]), x:min(x+w, frame.shape[1])] = glasses_new

        cv2.imshow(winname, frame)
    else:
        cv2.imshow(winname, frame)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    sleep(0.001)

camera.release()
cv2.destroyAllWindows()






