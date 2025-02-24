import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face

def negate(B):
    return B * -1

def neighbours4(y, x):
    return (y, x-1),(y, x+1),(y-1, x),(y+1, x)

def neighboursX(y,x):
    return (y-1, x-1), (y-1, x+1), (y+1, x+1), (y+1, x-1)

def neighbours8(y,x):
    return neighboursX(y, x) + neighbours4(y, x)

def search(LB, label, y, x):
    LB[y, x] = label
    for ny, nx in neighbours4(y, x):
        px = LB[ny, nx]
        if px == -1:
            search(LB, label, ny, nx)

def recursive_label(B):
    LB = negate(B)
    label = 0
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            px = LB[y,x]
            if px == -1:
                label += 1
                search(LB, label, y, x)
    return LB

image = np.zeros((20, 20), dtype='int32')

image[1:-1, -2] = 1

image[1, 1:5] = 1
image[1, 7:12] = 1
image[2, 1:3] = 1
image[2, 6:8] = 1
image[3:4, 1:7] = 1

image[7:11, 11] = 1
image[7:11, 14] = 1
image[10:15, 10:15] = 1

image[5:10, 5] = 1
image[5:10, 6] = 1

from skimage.draw import disk
from sys import getrecursionlimit, setrecursionlimit
setrecursionlimit(300000)
print(getrecursionlimit())


rr, cc = disk((500, 500), 300)
image = np.zeros((1000, 1000))
image[rr, cc] = 1

img = recursive_label(image)

plt.imshow(img)
plt.show()