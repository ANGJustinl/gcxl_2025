# 24.9.22 优化了参数显示 | 对内存占用更小
import cv2
import torch
from logger import logger
from picamera2 import Picamera2
from ultralytics import YOLO

from utils import random_color

model = YOLO("Vision/models/half_yolo11s_openvino_model", task="detect")
logger.info("Pre-trained YOLOv10s Model loaded")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Device using: {device}")


def Predict(model, img, classes=[], min_conf=0.5, device="cpu"):
    """
    Using Predict Model to predict objects in img.

    Input classes to choose which to output.

    eg. Predict(chosen_model, img_input, classes=[human], min_conf=0.5)
    """
    if classes:
        results = model.predict(
            img, classes=classes, conf=min_conf, device=device, stream=True
        )
    else:
        results = model.predict(img, conf=min_conf, device=device, stream=True)
    return results


def Predict_and_detect(
    model,
    img,
    classes=[],
    min_conf=0.5,
    rectangle_thickness=2,
    text_thickness=1,
    device="cpu",
):
    """
    Using Predict Model to predict objects in img and detect the objects out.

    Input classes to choose which to output.

    eg. Predict_and_detect(chosen_model, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1)
    """
    results = Predict(model, img, classes, min_conf=min_conf, device=device)
    for result in results:
        for box in result.boxes:
            left, top, right, bottom = (
                int(box.xyxy[0][0]),
                int(box.xyxy[0][1]),
                int(box.xyxy[0][2]),
                int(box.xyxy[0][3]),
            )
            confidence = box.conf.tolist()[0]
            label = int(box.cls[0])
            color = random_color(label)
            cv2.rectangle(
                img,
                (left, top),
                (right, bottom),
                color=color,
                thickness=rectangle_thickness,
                lineType=cv2.LINE_AA,
            )
            caption = f"{result.names[label]} {confidence:.2f}"
            w, h = cv2.getTextSize(caption, 0, 1, 2)[0]
            cv2.rectangle(
                img, (left - 3, top - 33), (left + w + 10, top), color, -1
            )
            cv2.putText(
                img,
                caption,
                (left, top - 5),
                0,
                1,
                (0, 0, 0),
                text_thickness,
                16,
            )
    return img, results


picam2 = Picamera2()
picam2.start()
while True:
    # read frame
    # ret, frame = camera.read()
    image = picam2.capture_array("main")
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Perform object detection on an image
    result_img, _ = Predict_and_detect(
        model, image, classes=[], min_conf=0.5, device=device
    )

    # Display results
    cv2.imshow("YOLOv10 Inference", result_img)
    key = cv2.waitKey(1)
    if key == 32:  # 空格
        break

picam2.close()
cv2.destroyAllWindows()
