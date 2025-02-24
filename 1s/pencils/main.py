import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import os
import cv2
from pathlib import Path
from skimage.measure import moments_hu
from skimage.transform import rotate
import shutil
import random


def distance(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5

def extractor(region):
    area = np.sum(region.image) / region.image.size
    perimeter_value = region.perimeter / region.image.size
    euler = region.euler_number
    eccentricity = region.eccentricity

    orientation = region.orientation
    normalized_image = rotate(region.image, -np.degrees(orientation), resize=False)


    moments = moments_hu(normalized_image)
    axis_ratio = region.major_axis_length / (region.minor_axis_length or 1)
    aspect_ratio = min(region.image.shape[1], region.image.shape[0]) / max(region.image.shape[1], region.image.shape[0])
    compactness = (4 * np.pi * region.area) / (region.perimeter or 1) ** 2

    features = np.array([
        area, perimeter_value, euler, eccentricity,
        aspect_ratio, axis_ratio, compactness, *moments
    ])

    return features

def classificator(regions):
    tests_number = 2
    match_percent = 10
    classes = {}
    classes_id = 1
    print("\nClassification...")
    for id, region in regions:
        v = extractor(region)
        if not classes:
            classes[classes_id] = {}
            classes[classes_id][0] = [1, [region]]
            classes[classes_id][id] = [1, [region]]
            classes_id += 1
        else:
            not_in_classes = True
            keys = list(classes.keys())
            for key in keys:
                class_test_all = classes[key][0][1]

                if len(class_test_all) > tests_number:
                    random.shuffle(class_test_all)
                    class_test_all = class_test_all[:tests_number]

                for class_test in class_test_all:
                    class_v = extractor(class_test)
                    if distance(v, class_v) <= match_percent:
                        classes[key][0][0] += 1
                        classes[key][0][1].append(region)

                        if id in classes[key].keys():
                            classes[key][id][0] += 1
                            classes[key][id][1].append(region)
                        else:
                            classes[key][id] = [1, [region]]
                        not_in_classes = False
                        break

            if not_in_classes:
                classes[classes_id] = {}
                classes[classes_id][0] = [1, [region]]
                classes[classes_id][id] = [1, [region]]
                classes_id += 1
    return classes


def save_classes_img(classes, dir_name = "Classificated"):
    path_dir = Path(dir_name)

    if path_dir.exists():
        shutil.rmtree(path_dir)
    path_dir.mkdir(exist_ok=True)

    for key in classes.keys():
        i = 1
        classes_dir = dir_name + f"/{key}"
        path = Path(classes_dir)
        path.mkdir(exist_ok=True)

        for id in classes[key].keys():
            if id != 0:
                for region in classes[key][id][1]:
                    plt.cla()
                    plt.title(f"Class -{key}, file - {id}")
                    plt.imshow(region.image)
                    plt.savefig(path/ f"{i}-{id}.png")
                    i += 1



directory = "images/"
files = os.listdir(directory)

length = len(files)
files_sort = [0]*length
for file in files:
    id = int(file[5:-5]) - 1
    files_sort[id] = file

percent = 0.005

regions_marked = []
print("Extracting...")
for file in files_sort:
    image = cv2.imread(directory + file)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=10)
    thresh = cv2.erode(thresh, None, iterations=5)

    labeled = label(thresh)
    regions = regionprops(labeled)

    img_size = thresh.size
    for region in regions:
        if region.area > img_size * percent:
            regions_marked.append([file, region])


regions_classified = classificator(regions_marked)
save_classes_img(regions_classified)