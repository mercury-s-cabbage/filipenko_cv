import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face

def neighbours2(y, x):
    return (y, x-1), (y-1, x)

def exist(B, nbs):
    left, top = nbs
    if left[0] >= 0 and left[0] < B.shape[1] and left[1] >= 0 and left[1] < B.shape[0]:
        if B[left] == 0:
            left = None
    else:
     left = None

    if top[0] >= 0 and top[0] < B.shape[1] and top[1] >= 0 and top[1] < B.shape[0]:
        if B[top] == 0:
            top: None
    else:
        top = None



def two_pass(B):
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype="unit")
    label = 1
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y,x] != 0:
                nbs = neighbours2(y, x)
                print(exist(B, nbs))
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