import torch
from logger import logger
from picamera2 import Picamera2
from ultralytics import YOLO

from vision import *


def main():
    # Load pre-trained Model
    model = YOLO("models/best_ang_openvino_model", task="detect")
    logger.info("Pre-trained YOLOv11s Model loaded")

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )  # 可惜没cuda
    logger.info(f"Device using: {device}")

    # Initialize camera
    picam2 = Picamera2()
    picam2.start()
    while True:
        # read frame
        # ret, frame = camera.read()
        image = picam2.capture_array("main")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Perform object detection on an image
        result_img, _ = Predict_and_detect(
            model, image, classes=[], min_conf=0.7, device=device
        )

        # Display results
        cv2.imshow("YOLOv11 Inference", result_img)
        key = cv2.waitKey(1)
        if key == 32:  # 空格
            break

    picam2.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
