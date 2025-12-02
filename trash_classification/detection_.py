# ANG 24.12.1
import time
from logger import logger
from picamera2 import Picamera2
from ultralytics import YOLO

from uart import UARTCommunication
from vision import *


def classify(
    classify_time: int = 10, query_time: float = 0.3, confidence_threshold=0.7
) -> dict:
    """
    This function takes a picture using the PiCamera2 module and performs object detection using the YOLOv11s model.
    It returns a dictionary containing the class and confidence of the detected object.
    :param classify_time: The number of times to take a picture and perform object detection.
    :param confidence_threshold: The minimum confidence level required for an object to be detected.
    :return: A dictionary containing the class and confidence of the detected object.
    """
    # Load pre-trained Model
    model = YOLO("models/trash_openvino_model", task="detect")
    logger.info("Pre-trained YOLOv11s Model loaded")

    # Initialize camera
    picam2 = Picamera2()
    picam2.start()

    results_list = []
    image_dict = {}
    # Perform object detection on an image and get the class of the detected object
    for i in range(classify_time):
        image = picam2.capture_array("main")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_dict[i] = image

        results = Predict(model, image)
        results_list.append(results)
        logger.info(f"Detection {i+1}/{classify_time} complete")
        time.sleep(query_time)

    # Loop through the results and print the class and confidence
    confident_objects = {}
    for i in results_list:
        for result in results:
            for box in result.boxes:
                confidence = box.conf.tolist()[0]
                if confidence < confidence_threshold:
                    continue
                image = image_dict[i]
                label = int(box.cls[0])
                cv2.imwrite(f"detections/{i}_{label}_{confidence}.jpg", image)
                confident_objects[result.names[label]] = confidence
    image_dict.clear()

    # Sort the dictionary by confidence in descending order
    confident_objects = dict(
        sorted(
            confident_objects.items(), key=lambda item: item[1], reverse=True
        )
    )

    # Close the camera and return the dictionary of confident objects
    picam2.close()
    return confident_objects


if __name__ == "__main__":
    print(classify())
