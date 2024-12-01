import torch
from logger import logger
from picamera2 import Picamera2
from ultralytics import YOLO

from uart import UARTCommunication
from vision import *


def classify(image, confidence_threshold=0.7):
    # Load pre-trained Model
    model = YOLO("models/trash_openvino", task="detect")
    logger.info("Pre-trained YOLOv11s Model loaded")

    # Initialize camera
    picam2 = Picamera2()
    picam2.start()
    
    image = picam2.capture_array("main")
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Perform object detection on an image and get the class of the detected object
    results = Predict(model, image, stream=False)

    # Loop through the results and print the class and confidence
    confident_objects = []
    for result in results:
        for box in result.boxes:
            confidence = box.conf.tolist()[0]
            if confidence < confidence_threshold:
                continue
            label = int(box.cls[0])
            caption = f"{result.names[label]} {confidence:.2f}"
            logger.info(caption)
            confident_objects.append(caption)
    picam2.close()
    return confident_objects


if __name__ == "__main__":
    print(classify())