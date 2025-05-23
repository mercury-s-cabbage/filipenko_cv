import math
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from pathlib import Path
import cv2
import time


def calculate_angle(pt1, vertex, pt2):
    angle_rad_1 = np.arctan2(pt2[1] - vertex[1], pt2[0] - vertex[0])
    angle_rad_2 = np.arctan2(pt1[1] - vertex[1], pt1[0] - vertex[0])
    diff_angle = np.rad2deg(angle_rad_1 - angle_rad_2)
    if diff_angle < 0:
        diff_angle += 360
    if diff_angle > 180:
        diff_angle = 360 - diff_angle
    return diff_angle


def analyze_knee_angle(frame_img, kpts):
    left_ear_visible = kpts[3][0] > 0 and kpts[0][1] > 0
    right_ear_visible = kpts[4][0] > 0 and kpts[0][1] > 0

    left_hip_pt = kpts[11]
    right_hip_pt = kpts[12]
    left_knee_pt = kpts[13]
    right_knee_pt = kpts[14]
    left_ankle_pt = kpts[15]
    right_ankle_pt = kpts[16]

    try:
        if left_ear_visible and not right_ear_visible:
            knee_angle = calculate_angle(left_hip_pt, left_knee_pt, left_ankle_pt)
            knee_point = left_knee_pt
        else:
            knee_angle = calculate_angle(right_hip_pt, right_knee_pt, right_ankle_pt)
            knee_point = right_knee_pt

        pos_x, pos_y = int(knee_point[0]) + 10, int(knee_point[1]) + 10
        cv2.putText(frame_img, f"{int(knee_angle)}", (pos_x, pos_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (25, 25, 255), 1)
        return int(knee_angle)

    except ZeroDivisionError:
        return None


def main():
    base_path = Path(__file__).parent / "data"
    yolo_model_path = base_path / "yolo11n-pose.pt"

    pose_model = YOLO(str(yolo_model_path))

    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Cannot open camera")
        return

    cv2.namedWindow("IMG", cv2.WINDOW_NORMAL)

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_writer = cv2.VideoWriter("videos/out.mp4",
                                   cv2.VideoWriter_fourcc(*"mp4v"),
                                   20, (width, height))

    prev_time = time.time()
    last_motion_time = time.time()
    movement_flag = False
    repetition_count = 0

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        video_writer.write(frame)

        current_time = time.time()
        fps = 1 / (current_time - prev_time) if current_time != prev_time else 0
        prev_time = current_time

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (25, 255, 25), 1)

        detection_results = pose_model(frame)

        cv2.imshow("IMG", frame)

        key_pressed = cv2.waitKey(1)
        if key_pressed == ord("q"):
            break

        if not detection_results:
            continue

        first_result = detection_results[0]
        keypoints_list = first_result.keypoints.xy.tolist()
        if not keypoints_list:
            continue

        keypoints = keypoints_list[0]
        if not keypoints:
            continue

        annotator = Annotator(frame)
        annotator.kpts(first_result.keypoints.data[0], first_result.orig_shape, 5, True)
        annotated_frame = annotator.result()

        knee_angle_value = analyze_knee_angle(annotated_frame, keypoints)
        if knee_angle_value is None:
            continue

        if movement_flag and knee_angle_value > 160:
            movement_flag = False
            repetition_count += 1
            last_motion_time = time.time()
        elif not movement_flag and knee_angle_value < 140:
            movement_flag = True
            last_motion_time = time.time()

        if time.time() - last_motion_time >= 10:
            repetition_count = 0

        cv2.putText(annotated_frame, f"Count = {repetition_count}", (10, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (25, 255, 25), 1)
        cv2.imshow("Pose", annotated_frame)

    video_writer.release()
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
