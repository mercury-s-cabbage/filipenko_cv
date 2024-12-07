import cv2
import matplotlib.pyplot as plt
import numpy as np

news = cv2.imread("news.jpg")
cheb = cv2.imread("cheburashka.jpg")

dest_pts = np.float32([[17,25],[432,55],[433,269],[40,294]])
src_pts = np.float32([[0,0],
                      [cheb.shape[1], 0],
                      [cheb.shape[1], cheb.shape[0]],
                      [0, cheb.shape[0]]])

M = cv2.getPerspectiveTransform(src_pts, dest_pts)
print(M)
perspect_img = cv2.warpPerspective(cheb, M, news.shape[:2][::-1])

gray = cv2.cvtColor(perspect_img, cv2.COLOR_RGB2GRAY)
ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

bg = cv2.bitwise_and(news, news, mask=cv2.bitwise_not(mask))
fg = cv2.bitwise_and(perspect_img, perspect_img, perspect_img, mask=mask)
result = cv2.add(bg, fg)

# plt.imshow(cv2.cvtColor(perspect_img, cv2.COLOR_BGR2RGB)) # GRB
# plt.show()

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", result)
cv2.waitKey()
cv2.destroyAllWindows()