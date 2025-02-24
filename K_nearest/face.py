import cv2
import matplotlib.pyplot as plt
import numpy as np

haar_cascade = "haarcascades/haarcascade_eye_tree_eyeglasses.xml"
lbp_cascade = "lbpcascades/lbpcascade_frontalface.xml"

face = cv2.CascadeClassifier(haar_cascade)
glasses = cv2.imread("dealwithit.png")
lbp = cv2.CascadeClassifier(lbp_cascade)

def detector(img, classifier, scaleFactor=None, minNeighbors=None):
    result = img.copy()
    rects = classifier.detectMultiScale(result, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
    if len(rects) == 2:
        (x1, y1, w1, h1) = rects[0]
        (x2, y2, w2, h2) = rects[1]
        return (x1, y1, abs(x1-x2)+w2, abs(y1-y2)+h2)
    return


# sheldon = cv2.imread("cooper.jpg")
# solvay = cv2.imread("solvay-conference.jpg")
#
# plt.figure()
# plt.imshow(detector(sheldon, face, 1.2, 5))
# plt.figure()
# plt.imshow(detector(solvay, lbp, 1.2, 5))
# plt.show()

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)
while camera.isOpened():
    ret, frame = camera.read()
    cv2.imshow("Camera", frame)

    data = detector(frame, face, 1.2, 5)
    if data:
        (x, y, w, h) = data

        glasses_new = np.where(glasses[0: h if y+h < frame.shape[0] else frame.shape[0] - y, 0: w if x+w < frame.shape[1] else frame.shape[1] - x,] == 0,
                               glasses[0: h if y+h < frame.shape[0] else frame.shape[0] - y, 0: w if x+w < frame.shape[1] else frame.shape[1] - x,],
                               frame[y:min(y+h, frame.shape[0]), x:min(x+w, frame.shape[1])])

        frame[y:min(y + h, frame.shape[0]), x:min(x + w, frame.shape[1])] = glasses_new

    cv2.imshow("Camera", detector(frame, face, 1.2, 5))

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()