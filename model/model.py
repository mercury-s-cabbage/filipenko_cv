import cv2
from tensorflow.keras.models import load_model
import numpy as np
model = load_model("model.keras")
model.summary()

cv2.namedWindow("Paint")
canvas = np.zeros((280, 280), dtype="uint8")
drawing = False

def draw_callback(event, x, y, *args):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    if event == cv2.EVENT_LBUTTONUP:
        drawing = False
    if event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(canvas, (x,y), 10, 255, -1)

cv2.setMouseCallback("Paint", draw_callback)

while True:
    cv2.imshow("Paint", canvas)
    key = cv2.waitKey(1)
    if key==27:
        break
    if key==ord("c"):
        canvas[:] = 0
    if key==ord("p"):
        image = cv2.resize(canvas, (28, 28)).reshape(1, 28, 28, 1)
        prediction = model.predict(image)
        print(prediction)