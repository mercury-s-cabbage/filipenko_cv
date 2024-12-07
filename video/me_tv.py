from itertools import combinations
import cv2
import matplotlib.pyplot as plt
import numpy as np

import cv2

news = cv2.imread("news.jpg")

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

ret, cheb = camera.read()
dest_pts = np.float32([[17,25],[432,55],[433,269],[40,294]])
src_pts = np.float32([[0,0],
                      [cheb.shape[1], 0],
                      [cheb.shape[1], cheb.shape[0]],
                      [0, cheb.shape[0]]])

M = cv2.getPerspectiveTransform(src_pts, dest_pts)
print(M)


while camera.isOpened():
    ret, cheb = camera.read()

    perspect_img = cv2.warpPerspective(cheb, M, news.shape[:2][::-1])

    gray = cv2.cvtColor(perspect_img, cv2.COLOR_RGB2GRAY)
    ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    bg = cv2.bitwise_and(news, news, mask=cv2.bitwise_not(mask))
    fg = cv2.bitwise_and(perspect_img, perspect_img, perspect_img, mask=mask)
    result = cv2.add(bg, fg)



    cv2.imshow("Camera", result)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()