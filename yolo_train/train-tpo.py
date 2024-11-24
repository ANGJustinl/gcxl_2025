import time
import torch
import matplotlib.pyplot as plt

from ray import tune
from ray.tune.schedulers import ASHAScheduler
from ultralytics import YOLO


def train_detection_model(
    data_yaml_path,
    epochs=100,
    imgsz=640,
    batch_size=-1,
    space={},
    scheduler={},
):
    """
    训练检测模型
    :param data_yaml_path: 数据集的yaml文件路径
    :param epochs: 训练的轮数
    :param imgsz: 输入图像的尺寸
    :param batch_size: 训练的batch大小，-1表示自适应
    """
    # Using GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 加载模型 Using device
    model = YOLO("./yolov11.yaml").load("model/yolo11n.pt").to(device)
    now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    result_grid = model.tune(
        data=data_yaml_path,
        param_space=space,
        scheduler=scheduler,
        epochs=epochs,
        use_ray=True,
        device=device,
        imgsz=imgsz,
        batch_size=batch_size,
    )

    # 打印结果
    for i, result in enumerate(result_grid):
        print(
            f"Trial #{i}: Configuration: {result.config}, Last Reported Metrics: {result.metrics}"
        )
        with open(f"./results/trial{now_time}.txt", "w") as f:
            f.write(
                f"Trial #{i}: Configuration: {result.config}, Last Reported Metrics: {result.metrics}"
            )

    for i, result in enumerate(result_grid):
        plt.plot(
            result.metrics_dataframe["training_iteration"],
            result.metrics_dataframe["mean_accuracy"],
            label=f"Trial {i}",
        )

    plt.xlabel("Training Iterations")
    plt.ylabel("Mean Accuracy")
    plt.legend()
    # 保存图像
    plt.savefig(f"./results/accuracy_{now_time}.png")
    plt.show()

    return True


if __name__ == "__main__":
    path = "./datasets/"  # 数据集的路径
    # 超参数搜索空间
    search_space = {
        "lr": tune.loguniform(1e-5, 1e-3),  # 学习率
        "batch_size": tune.choice([16, 32, 64]),  # 批次大小
        "epochs": tune.choice([10, 20, 30]),  # 训练轮数
    }
    # 调度器，用于控制优化过程
    scheduler = ASHAScheduler(
        metric="accuracy",
        mode="max",
        max_t=50,
        grace_period=1,
        reduction_factor=2,
    )

    train_detection_model(
        path, epochs=8, imgsz=640, space=search_space, scheduler=scheduler
    )
