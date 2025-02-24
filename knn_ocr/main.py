import numpy as np
import matplotlib.pyplot as plt
import random
from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
import cv2

def binarization(image):
    if len(image.shape) == 3:
      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
      gray = image

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

dir = Path("train")
task_dir = Path("task")
letter_height = 130
letter_width = 160

folders = sorted([f for f in dir.iterdir()])

letters = {}
for folder in folders:
    letters[folder.name[-1]] = [cv2.imread(str(file)) for file in folder.iterdir()]

for letter in letters.keys():
    for i, image in enumerate(letters[letter]):
        bin_image = binarization(image)
        letters[letter][i] = cv2.resize(bin_image, (letter_width, letter_height))

X_train = []
Y_train = []
for letter in letters.keys():
    for image in letters[letter]:
        X_train.append(image.flatten())
        Y_train.append(letter)

knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(X_train, Y_train)

task_dir = Path("task")
task_files = sorted([file for file in task_dir.iterdir() if file.is_file()])

test_data = []
for file in task_files:
  image = cv2.imread(str(file))
  binary_image = binarization(image)

  binary_image_re = binary_image.copy()
  kernel = np.ones((20, 1), np.uint8)
  dilay_image = cv2.dilate(binary_image_re, kernel, iterations=1)
  kernel = np.ones((20, 1), np.uint8)
  eroded_image = cv2.erode(dilay_image, kernel, iterations=1)

  # cv2_imshow(eroded_image)

  contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  task_letters = []
  for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    task_letters.append((x, y, cv2.resize(binary_image[y:y+h, x:x+w], (letter_width, letter_height))))

  task_letters.sort(key=lambda arr: (arr[0], arr[1]))

  test_data.append([arr[2] for arr in task_letters])



for i, words in enumerate(test_data):
  for letter_image in words:
    print(knn.predict([letter_image.flatten()]), end="")
  print()
