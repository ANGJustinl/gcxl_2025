# 24.9.22 优化了参数显示 | 对内存占用更小
import cv2
import torch
import logging

from ultralytics import YOLO

from vision import *


logger = logging.getLogger()

model = YOLO("./models/best_ang.pt")
logger.info("Pre-trained Model loaded")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Device using: {device}")


camera = cv2.VideoCapture(0)
while True:
    # read frame
    ret, frame = camera.read()

    # Perform object detection on an image
    result_img, _ = Predict_and_detect(
        model, frame, classes=[], min_conf=0.5, device=device
    )

    # Display results
    cv2.imshow("YOLO Inference", result_img)
    key = cv2.waitKey(1)
    if key == 32:  # 空格
        break

camera.release()
cv2.destroyAllWindows()
