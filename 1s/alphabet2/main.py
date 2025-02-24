import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from pathlib import Path
from scipy.ndimage import binary_dilation


def recognize(region):
    if region.image.mean() == 1.0:
        return "minus"
    else:
        image = region.image.copy()
        struct = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        open_image = binary_dilation(image, struct)
        enumber = euler_number(open_image)
        if enumber == -1:
            have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1]//2], 0) == 1) > 3
            if have_vl:
                return "B"
            else:
                return "8"
        elif enumber == 0:
            area = np.sum(region.image) / region.image.size
            if area<=0.47:
                return "A"
            elif area<=0.55:
                return "P"
            else:
                have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1] // 2], 0) == 1) > 3
                if have_vl:
                    return "D"
                else:
                    return "0"
        else:
            have_vl = np.sum(np.mean(region.image, 0) == 1) > 3
            if have_vl:
                return "1"
            else:
                if region.eccentricity < 0.4:
                    return "star"
                else:
                    image = region.image.copy()
                    image[0, :] = 1
                    image[-1, :] =  1
                    image[:, 0] = 1
                    image[:, -1] = 1
                    enumber = euler_number(image)
                    if enumber == -1:
                        return "slash"
                    elif enumber == -3:
                        return "X"
                    else:
                        return"W"
    return "None"




im = plt.imread("symbols.png")[:, :, :3].mean(2)
im[im > 0] = 1
labeled = label(im)
regions = regionprops(labeled)

result = defaultdict(lambda: 0)
i = 0



for region in regions:
    symbol = recognize(region)
    result[symbol] += 1
    plt.cla()
    plt.title(f"Symbol - {symbol}")
    plt.imshow(region.image)

    path = Path(f"{symbol}")
    path.mkdir(exist_ok=True)

    plt.savefig(path/ f"image_{i}.png")
    i+=1


print(result)