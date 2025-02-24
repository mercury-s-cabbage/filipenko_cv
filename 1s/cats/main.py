import cv2

cat = cv2.imread("cat.png")

cat1 = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)
cat2 = cv2.imread("cat2.png", cv2.IMREAD_GRAYSCALE)

diff = cv2.absdiff(cat1, cat2)
tresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
tresh = cv2.dilate(tresh, None, iterations=2)

contours, hierarchy = cv2.findContours(tresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(cat, (x,y), (x+w, y+h), (0, 255, 0), 2)
cv2.putText(cat, f"Differences = {len(contours)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0))


cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.namedWindow("Difference", cv2.WINDOW_NORMAL)
cv2.imshow("Difference", diff)
cv2.imshow("Original", cat)
cv2.waitKey()
cv2.destroyAllWindows()