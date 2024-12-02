# 24.9.22 优化了参数显示 | 对内存占用更小
import cv2

from .utils import random_color


def Predict(model, img, classes=[], min_conf=0.5, device="cpu", stream=True):
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
            cv2.rectangle(img, (left - 3, top - 33), (left + w + 10, top), color, -1)
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
