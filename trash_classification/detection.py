import cv2
import time
import logging

from ultralytics import YOLO

# 设置日志级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def capture_and_detect(model_path, max_confidence=0, duration=3) -> dict:
    """
    使用摄像头捕获视频，并使用YOLO进行检测。

    :param model_path: YOLO模型路径
    :param max_confidence: 置信度阈值，默认为0
    :param duration: 录制视频的时长（秒），默认为3秒
    :return: {"Status": True, "Class": "类别名称", "Confidence": 置信度}
    """
    # 加载YOLO模型
    model = YOLO(model_path)

    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.info("无法打开摄像头")
        return

    # 获取视频参数
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(fps * duration)
    best_detection = None

    logger.warning(f"现在开始录制 {duration} 秒视频...")
    start_time = time.time()

    frames = []
    while len(frames) < frame_count:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

        # 使用YOLO进行检测
        results = model(frame)

        # 获取当前帧中置信度最高的检测结果
        for result in results:
            if len(result.boxes.conf) > 0:
                conf = float(result.boxes.conf.max())
                if conf > max_confidence:
                    max_confidence = conf
                    # 获取类别名称
                    class_id = int(
                        result.boxes.cls[result.boxes.conf.argmax()]
                    )
                    class_name = model.names[class_id]
                    best_detection = (class_name, conf)

        if time.time() - start_time >= duration:
            break

    # 释放摄像头
    cap.release()

    if best_detection:
        logger.info(f"\n检测结果:")
        logger.info(f"类别: {best_detection[0]}")
        logger.info(f"置信度: {best_detection[1]:.2%}")
        return {
            "Status": True,
            "Class": best_detection[0],
            "Confidence": best_detection[1],
        }
    else:
        logger.error("未检测到任何对象")
        return {"Status": False, "Class": None, "Confidence": None}


if __name__ == "__main__":
    model_path = "./models/best_ang_openvino_model"
    res = capture_and_detect(model_path)
    logger.info(res)
