import matplotlib
import numpy as np
import matplotlib.pyplot as plt

extern_mask = np.array([[[0,0], [0,1]],
                       [[0,0], [1,0]],
                       [[0,1], [0,0]],
                       [[1,0], [0,0]]])

cross_mask = np.array([[[0,1],[1,0]],
                       [[1,0],[0,1]]])

intern_mask = np.logical_not(extern_mask).astype("int")

def match(a, masks):
    for mask in masks:
        if np.all(a == mask):
            return True
    return False


def coun_objects(B):
    intern = 0
    extern = 0
    for y in range(0, B.shape[0]-1):
        for x in range(0, B.shape[1]-1):
            sub = B[y:y+2, x:x+2]
            if match(sub, extern_mask):
                extern += 1
            if match(sub, intern_mask):
                intern += 1
            if match(sub, cross_mask):
                extern += 2
    return (extern - intern) / 4


plt.figure()

image = np.load(f"cex2.npy.txt")
plt.subplot(131)
plt.imshow(image[:,:,0])
plt.title(f"{coun_objects(image[:,:,0])}")

plt.subplot(132)
plt.imshow(image[:,:,1])
plt.title(f"{coun_objects(image[:,:,1])}")

plt.subplot(133)
plt.imshow(image[:,:,2])
plt.title(f"{coun_objects(image[:,:,2])}")

plt.show()