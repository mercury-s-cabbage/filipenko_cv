import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.morphology import binary_dilation, disk
import numpy as np

# Загрузка изображения
im = plt.imread("бин.png")
# Преобразование в оттенки серого
gray = np.mean(im, axis=2)

# Определение порогов бинаризации
thresh = threshold_otsu(gray) * 0.6  # Уменьшение порога для большего количества белых оттенков

# Бинаризация изображения
binary = np.zeros_like(gray)
binary[gray > thresh] = 1  # Белый фон

# Наращивание (уменьшенное)
dilated = binary_dilation(binary, disk(1))

# Отображение результатов
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
ax[0].imshow(gray, cmap="gray")
ax[0].set_title("Градации серого")
ax[0].axis("off")
plt.imsave("gray_image.png", gray, cmap="gray")

ax[1].imshow(binary, cmap="gray")
ax[1].set_title("Бинаризированное изображение")
ax[1].axis("off")
plt.imsave("binary_image.png", binary, cmap="gray")

ax[2].imshow(dilated, cmap="gray")
ax[2].set_title("Наращенное изображение")
ax[2].axis("off")
plt.imsave("dilated_image.png", dilated, cmap="gray")

plt.show()