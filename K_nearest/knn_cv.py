import cv2
import numpy as np
import matplotlib.pyplot as plt

n = 1000
#np.random.seed(20)

xk1 = 100 + np.random.randint(-25, 25, n)
yk1 = 100 + np.random.randint(-25, 25, n)

xk2 = 150 + np.random.randint(-25, 25, n)
yk2 = 150 + np.random.randint(-25, 25, n)

rk1 =np.repeat(1, n)
rk2 =np.repeat(2, n)

knn = cv2.ml.KNearest_create()
train = np.stack([np.hstack([xk1, xk2]), np.hstack([yk1, yk2])]).T.astype("f4")
response = np.hstack([rk1, rk2]).reshape(-1, 1).astype("f4")
print(response.shape)

knn.train(train, cv2.ml.ROW_SAMPLE, response)

new_point = (125, 125)
ret, results, neightbor, dist = knn.findNearest(np.array(new_point).astype("f4").reshape(1, 2), 5)

print(results, neightbor, dist)

plt.scatter(xk1, yk1, 80, "r", "^")
plt.scatter(xk2, yk2, 80, "b", "s")
if ret == 2:
    plt.scatter(new_point[0], new_point[1], 80, "g", "s")
else:
    plt.scatter(new_point[0], new_point[1], 80, "g", "^")
plt.show()