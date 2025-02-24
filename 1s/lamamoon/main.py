import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, sobel
from skimage.measure import label, regionprops
import numpy as np
from skimage.segmentation import flood_fill

'''def fill(binary):
    flag = 0
    for row in binary:
        for i in range(1, len(row)-1):
            if row[i] == 0 and row[i-1] != 0 and flag<2:
                while
            elif row[i] != 0 and row[i-1] != 0:
                flag = 0


    return binary'''

im = plt.imread("lama_on_moon.png")
im = im[80:-40, 60:-40]

gray = np.mean(im, 2)
conts = sobel(gray)
tresh = threshold_otsu(conts)

binary = conts > tresh
labeled = label(binary)
for region in regionprops(labeled):
    if region.area < 200 or region.perimeter < 1000:
        binary[np.where(labeled == region.label)] = 0


new_labled = label(binary)
regions = regionprops(new_labled)
cy, cx = regions[0].centroid
new_binary = flood_fill(binary, (int(cy), int(cx)), 1)


binary = conts > tresh
plt.imshow(new_binary * binary, cmap="gray")
plt.show()
