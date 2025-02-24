import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from pathlib import Path
from scipy.ndimage import binary_dilation


def recognize(region):
        image = region.image.copy()
        struct = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        open_image = binary_dilation(image, struct)
        enumber = euler_number(open_image)
        #if area<100:
            #return "L"
        #elif area > 410:
            #return "R"
        if enumber<=0:
            perimeter = region.perimeter
            area = np.sum(region.image)
            eccentricity = region.eccentricity
            if eccentricity<0.40:
                return "D"
                #return "None"
            else:
                left = np.sum(region.image[:, :region.image.shape[1] // 2])
                right = np.sum(region.image[:, region.image.shape[1] // 2:])
                if right<left:
                    return "D"
                else:
                    return "R"

        else:
            have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1] // 2], 0) == 1) > 3
            if have_vl==0:
                return "J"
                #return "None"
            else:
                have_hl = np.sum(np.mean(region.image[-region.image.shape[0]//4:, :], 1) == 1) > 2
                if have_hl==0:
                    return "K"
                    #return "None"
                else:
                    return "L"
                    #return "None"




im = plt.imread("task3.png")[:, :, :3].mean(2)
im[im > 0] = 1 # бинаризируем
labeled = label(im)
print(labeled.max())
regions = regionprops(labeled)

result = defaultdict(lambda: 0)
i = 0



for region in regions:
    symbol = recognize(region)
    if symbol != "None":
        result[symbol] += 1
        plt.cla()
        plt.title(f"Symbol - {symbol}")
        plt.imshow(region.image)

        path = Path(f"{symbol}")
        path.mkdir(exist_ok=True)

        plt.savefig(path/ f"image_{i}.png")
        i+=1


print(result)