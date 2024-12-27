import os
import time
import cv2
import pymunk.pygame_util
import pygame

# Константы
WIDTH, HEIGHT = 300, 500
FPS = 30
IMAGE_PATH = "photo.jpg"
CONTOUR_UPDATE_INTERVAL = 1  # Проверка изменений каждые 1 секунду

# Функция для извлечения контуров
def extract_all_contours(image_path, scale_factor=1):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return []  # Если изображение не найдено
    original_height, original_width = img.shape
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)

    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    scale_x = WIDTH / original_width
    scale_y = HEIGHT / original_height
    scale = min(scale_x, scale_y)

    all_contours = [
        [(point[0][0] * scale, HEIGHT - point[0][1] * scale) for point in contour]
        for contour in contours
    ]
    return all_contours


# Инициализация Pygame и Pymunk
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
print(clock.get_fps())

space = pymunk.Space()
space.gravity = (0, 900)

# Визуализация
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Параметры шарика
ball_radius = 15
ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, ball_radius))
ball_body.position = (WIDTH // 2, ball_radius)
ball_body.velocity = (0, 0)
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.friction = 0.9
ball_shape.elasticity = 0.1
space.add(ball_body, ball_shape)

# Переменные для отслеживания изменения изображения
last_mod_time = os.path.getmtime(IMAGE_PATH)
last_update_time = time.time()

# Загрузка начальных контуров
contours = extract_all_contours(IMAGE_PATH)
static_bodies = []

# Функция для обновления контуров
def update_contours():
    global contours, static_bodies
    # Удаление старых объектов
    for body in static_bodies:
        space.remove(body)
    static_bodies = []

    # Добавление новых объектов
    for contour in contours:
        for i in range(len(contour) - 1):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            segment = pymunk.Segment(body, contour[i], contour[i + 1], 5)
            segment.friction = 0.9
            space.add(body, segment)
            static_bodies.append(body)

update_contours()

# Основной цикл
running = True
while running:
    current_time = time.time()

    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Проверка изменений изображения
    if current_time - last_update_time > CONTOUR_UPDATE_INTERVAL:
        mod_time = os.path.getmtime(IMAGE_PATH)
        if mod_time != last_mod_time:  # Если изображение изменилось
            last_mod_time = mod_time
            contours = extract_all_contours(IMAGE_PATH)
            update_contours()
        last_update_time = current_time

    # Обновление физики
    space.step(1 / FPS)

    # Отображение
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(FPS)
    print(clock.get_fps())

pygame.quit()
