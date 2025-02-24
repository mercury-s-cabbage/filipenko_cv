import cv2
import numpy as np


def get_hsv_from_camera():
    # Открыть камеру
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Не удалось открыть камеру")
        return

    print("Нажмите 'q' для выхода. Щелкните левой кнопкой мыши, чтобы получить HSV.")

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Получить цвет пикселя
            pixel = frame[y, x]
            # Преобразовать в HSV
            hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]
            print(f"Координаты: ({x}, {y}), BGR: {pixel}, HSV: {hsv_pixel}")

    cv2.namedWindow("Camera")
    cv2.setMouseCallback("Camera", mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка при захвате изображения")
            break

        cv2.imshow("Camera", frame)

        # Нажмите 'q' для выхода
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    get_hsv_from_camera()
