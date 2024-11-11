import time
import torch
from ultralytics import YOLO

def train_detection_model(data_yaml_path, epochs=100, imgsz=640, batch_size=-1):
    '''
    训练检测模型
    :param data_yaml_path: 数据集的yaml文件路径
    :param epochs: 训练的轮数
    :param imgsz: 输入图像的尺寸
    :param batch_size: 训练的batch大小，-1表示自适应
    '''
    # Using GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 加载模型 Using device
    model = YOLO('./yolov11.yaml').load('model/yolo11n.pt')
    # 训练模型
    results = model.train(data=data_yaml_path,
                            epochs=epochs,
                            imgsz=imgsz, 
                            device=device, 
                            batch=batch_size,
                            workers=0,
                            format="engine",
                            dynamic=True)
    # 保存训练好的模型 (using time now as filename)
    model.save(f"output/{int(time.time())}_trained_model.pt")
    return True

if __name__ == "__main__":
    path = "./datasets/" # 数据集的路径
    train_detection_model(path, epochs=8, imgsz=640)