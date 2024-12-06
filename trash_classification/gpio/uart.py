# ANG 24.12.1
import serial
from logger import logger
import time


class UARTCommunication:
    """
    树莓派与其他设备的 UART 串口通信类
    """

    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def connect(self):
        """
        连接到串口
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
            )
            logger.info(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            raise Exception(f"Failed to connect to {self.port}: {e}")

    def send_data(self, data):
        """
        发送数据到串口
        :param data: 发送的字节数据
        """
        if self.serial and self.serial.is_open:
            if isinstance(data, int):
                data = chr(data)  # 将整数转换为字符
            self.serial.write(data.encode("utf-8"))
            logger.info(f"Sent: {data}")
        else:
            raise Exception("Serial port not open.")

    def receive_data(self):
        """
        从串口接收数据
        :return: 接收到的字符串数据
        """
        if self.serial and self.serial.is_open:
            if self.serial.in_waiting > 0:
                data = self.serial.readline().decode("utf-8").strip()
                logger.info(f"Received: {data}")
                return data
            return None
        else:
            raise Exception("Serial port not open.")

    def close(self):
        """
        关闭串口
        """
        if self.serial:
            self.serial.close()
            logger.warning("Serial connection closed.")


if __name__ == "__main__":
    # 示例使用
    uart = UARTCommunication(port="/dev/ttyUSB0", baudrate=9600)
    try:
        uart.connect()
        while True:
            for i in range(10):  # 发送0到9数字
                uart.send_data(i)
                response = uart.receive_data()
                if response:
                    logger.info(f"Response: {response}")
            time.sleep(0.5)

    except KeyboardInterrupt:
        logger.exception("Exiting program.")
    finally:
        uart.close()
