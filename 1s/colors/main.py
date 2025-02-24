import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
import numpy as np
import cv2
import statistics
print(cv2.getBuildInformation())
im = plt.imread("balls.png")

binary = im.mean(2)
binary[binary>0] = 1
labeled = label(binary)
regions = regionprops(labeled)

colors = []
im_hsv = rgb2hsv(im)
print(np.max(labeled))
for region in regions:
    cy, cx = region.centroid
    color = im_hsv[int(cy), int(cx)][0]
    colors.append(color)

k = 1
s = sorted(colors)
eps = s[1]-s[0]
print(eps)
for i in range(len(s)-1):
    if s[i+1] - s[i] > eps*2:
        k += 1

print(k)

plt.figure()
plt.plot(sorted(colors), "o")
plt.show()