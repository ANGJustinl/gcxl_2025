import RPi.GPIO as GPIO
import time


class ServoController:
    def __init__(self, servo1_pin, servo2_pin, power1_pin, power2_pin, frequency=50):
        """
        初始化舵机控制器

        Args:
            servo1_pin (int): 第一个舵机的信号针脚
            servo2_pin (int): 第二个舵机的信号针脚
            power1_pin (int): 第一个电源控制针脚
            power2_pin (int): 第二个电源控制针脚
            frequency (int): PWM频率，默认50Hz适用于大多数舵机
        """
        # 设置GPIO模式为BCM
        GPIO.setmode(GPIO.BCM)

        # 存储针脚信息
        self.servo_pins = [servo1_pin, servo2_pin]
        self.power_pins = [power1_pin, power2_pin]
        self.frequency = frequency

        # 初始化所有针脚为输出模式
        for pin in self.servo_pins + self.power_pins:
            GPIO.setup(pin, GPIO.OUT)

        # 初始化PWM对象
        self.servos = [
            GPIO.PWM(servo1_pin, frequency),
            GPIO.PWM(servo2_pin, frequency)
        ]

        # 启动PWM
        for servo in self.servos:
            servo.start(0)  # 初始占空比为0

        # 设置电源针脚为高电平（5V输出）
        for pin in self.power_pins:
            GPIO.output(pin, GPIO.HIGH)

    def angle_to_duty_cycle(self, angle):
        """
        将角度转换为占空比

        Args:
            angle (float): 目标角度（0-180度）

        Returns:
            float: 对应的占空比（2.5-12.5）
        """
        # MG995舵机的占空比范围通常是2.5%（0度）到12.5%（180度）
        return 2.5 + (angle / 180) * 10

    def set_angle(self, servo_index, angle):
        """
        设置指定舵机的角度

        Args:
            servo_index (int): 舵机索引（0或1）
            angle (float): 目标角度（0-180度）
        """
        if 0 <= servo_index < len(self.servos):
            duty_cycle = self.angle_to_duty_cycle(angle)
            self.servos[servo_index].ChangeDutyCycle(duty_cycle)
        else:
            raise ValueError("Invalid servo index")

    def cleanup(self):
        """
        清理GPIO资源
        """
        # 停止所有PWM
        for servo in self.servos:
            servo.stop()

        # 将所有电源针脚设为低电平
        for pin in self.power_pins:
            GPIO.output(pin, GPIO.LOW)

        # 清理GPIO设置
        GPIO.cleanup()


# 使用示例
if __name__ == "__main__":
    try:
        # 示例针脚配置（请根据实际接线修改）
        SERVO1_PIN = 18  # GPIO18
        SERVO2_PIN = 19  # GPIO19
        POWER1_PIN = 20  # GPIO20
        POWER2_PIN = 21  # GPIO21

        # 创建控制器实例
        controller = ServoController(
            servo1_pin=SERVO1_PIN,
            servo2_pin=SERVO2_PIN,
            power1_pin=POWER1_PIN,
            power2_pin=POWER2_PIN
        )

        # 测试舵机转动
        print("Moving servo 1 to 90 degrees...")
        controller.set_angle(0, 90)
        time.sleep(1)

        print("Moving servo 2 to 180 degrees...")
        controller.set_angle(1, 180)
        time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        controller.cleanup()
