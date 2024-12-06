import RPi.GPIO as GPIO
import time

# 定义 GPIO 引脚和参数
PWM_PIN = 18  # 树莓派 GPIO18 引脚 (BCM 模式)
PWM_FREQUENCY = 100  # PWM 频率 (Hz)
SUPPLY_VOLTAGE = 12  # 2PH78500A 输入电压 (V)
TARGET_VOLTAGE = 5  # 目标输出电压 (V)


# 初始化 GPIO 和 PWM
def setup_pwm():
    GPIO.setmode(GPIO.BCM)  # 使用 BCM 引脚编号
    GPIO.setup(PWM_PIN, GPIO.OUT)  # 设置 GPIO18 为输出模式

    # 初始化 PWM，设置频率
    pwm = GPIO.PWM(PWM_PIN, PWM_FREQUENCY)
    pwm.start(0)  # 初始占空比为 0%
    return pwm


# 调节 PWM 占空比
def set_fixed_voltage(pwm, target_voltage, supply_voltage):
    """
    设置固定输出电压。

    Args:
        pwm (GPIO.PWM): PWM 控制对象。
        target_voltage (float): 目标输出电压 (V)。
        supply_voltage (float): 模块供电电压 (V)。
    """
    if not (0 <= target_voltage <= supply_voltage):
        raise ValueError(f"Voltage must be between 0 and {supply_voltage}V")

    # 根据目标电压计算占空比
    duty_cycle = (target_voltage / supply_voltage) * 100
    pwm.ChangeDutyCycle(duty_cycle)
    print(
        f"Setting output to {target_voltage}V (Duty Cycle: {duty_cycle:.2f}%)"
    )


# 主程序
def main():
    pwm = None
    try:
        # 初始化 PWM
        pwm = setup_pwm()
        print("PWM initialized. Setting voltage...")

        # 设置固定输出电压
        set_fixed_voltage(pwm, TARGET_VOLTAGE, SUPPLY_VOLTAGE)

        # 保持输出，用户可用 Ctrl+C 停止程序
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        # 停止 PWM，清理 GPIO
        if pwm:
            pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup completed.")


if __name__ == "__main__":
    main()
