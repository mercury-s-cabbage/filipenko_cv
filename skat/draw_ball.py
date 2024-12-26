import cv2
import numpy as np
import pymunk
import pymunk.pygame_util
import pygame
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 300, 500  # Размер экрана
FPS = 60

fall_speed = 1800  # Увеличиваем скорость падения
smooth_factor = 0.1  # Фактор сглаживания

# Достаем координаты контура
def extract_all_contours(image_path, scale_factor=1):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Загрузка изображения в ЧБ
    original_height, original_width = img.shape
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)  # Масштабирование

    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)  # Бинаризация
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Вычисляем коэффициент масштаба
    scale_x = WIDTH / original_width
    scale_y = HEIGHT / original_height
    scale = min(scale_x, scale_y)  # Оставляем минимальный коэффициент для сохранения пропорций

    all_contours = []
    for contour in contours:
        # Преобразуем текущий контур в координаты Pymunk и масштабируем
        contour_points = [(point[0][0] * scale, HEIGHT - point[0][1] * scale) for point in contour]
        all_contours.append(contour_points)

    return all_contours


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Пространство Pymunk
space = pymunk.Space()
space.gravity = (0, 900)  # Гравитация вниз

# Загрузка и добавление контура
image_path = "photo.jpg"  # Путь к вашему изображению
contours = extract_all_contours(image_path)

if contours:
    for contour in contours:
        # Преобразуем текущий контур в сегменты
        for i in range(len(contour) - 1):
            # Создаем статическое тело
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            # Создаем сегмент, связанный с этим телом
            segment = pymunk.Segment(body, contour[i], contour[i + 1], 5)  # Толщина линии
            segment.friction = 0.9
            # Добавляем тело и сегмент в пространство
            space.add(body, segment)

# Параметры шарика
ball_radius = 15
ball_x = WIDTH // 2  # Центр по оси X
ball_y = ball_radius

# Добавляем шарик
ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
ball_body.position = (ball_x, ball_y)
ball_body.velocity = (0, fall_speed)  # Устанавливаем скорость падения
ball_shape = pymunk.Circle(ball_body, 15)  # Радиус 15
ball_shape.friction = 0.9
ball_shape.elasticity = 0.1
space.add(ball_body, ball_shape)

# Визуализация
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Основной цикл
previous_position = ball_body.position  # Начальная позиция шарика для сглаживания
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление физики
    space.step(1 / FPS)

    # Применение сглаживания: вычисляем новый position, используя smooth_factor
    ball_body.position = (
        previous_position[0] + (ball_body.position[0] - previous_position[0]) * smooth_factor,
        previous_position[1] + (ball_body.position[1] - previous_position[1]) * smooth_factor
    )

    # Сохраняем новую позицию для следующего сглаживания
    previous_position = ball_body.position

    # Отображение
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()