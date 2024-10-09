import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face

def consolve(image, mask):
    norm_mask = mask.astype("f4")# / mask.sum()
    result = np.zeros_like(image).astype("f4")
    for y in range(1, image.shape[0]-1):
        for x in range(1, image.shape[1]-1):
            sub = image[y-1:y+2, x-1:x+2]
            new_value = (sub * norm_mask).sum()
            result[y, x] = new_value
    return result[1:-1, 1:-1]

image = face(gray=True)
print(type(image))

mask = np.array([[-1,-1,-1],[2,2,2], [-1,-1,-1]])
image1 = consolve(image, mask)

mask = np.array([[-1,2,-1],[-1,2,-1], [-1,2,-1]])
image2 = consolve(image, mask)

mask = np.array([[2,-1,-1],[-1,2,-1], [-1,-1,2]])
image3 = consolve(image, mask)

plt.subplot(2, 2, 1)
plt.imshow(image1)

plt.subplot(2, 2, 2)
plt.imshow(image2)

plt.subplot(2, 2, 3)
plt.imshow(image3)

plt.show()




