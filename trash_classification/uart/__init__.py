# ANG 24.12.1
import time
import serial

from logger import logger


class UARTCommunication:
    """
    树莓派与其他设备的 UART 串口通信类
    """

    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, timeout=1):
        """
        初始化串口通信
        :param port: 串口设备路径
        :param baudrate: 波特率
        :param timeout: 读取超时时间（秒）
        """
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
        :param data: 发送的字节数据或字符串
        """
        if self.serial and self.serial.is_open:
            if isinstance(data, str):
                data = data.encode("utf-8")
            self.serial.write(data)
            logger.info(f"Sent: {data}")
        else:
            raise Exception("Serial port not open.")

    def send_int(self, data):
        """
        发送整数数据到串口
        :param data: 发送的整数数据
        """
        if self.serial and self.serial.is_open:
            if isinstance(data, int):
                num = data
                self.serial.write(num.to_bytes(2, "big"))
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

    def receive_int(self):
        """
        从串口接收整数数据
        :return: 接收到的整数数据
        """
        if self.serial and self.serial.is_open:
            if self.serial.in_waiting > 0:
                data = self.serial.read(2)
                num = int.from_bytes(data, "big")
                logger.info(f"Received: {num}")
                return num
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
            uart.send_int("1")
            response = uart.receive_int()
            if response:
                logger.info(f"Response: {response}")
            time.sleep(1)

            uart.send_int("2")
            response = uart.receive_int()
            if response:
                logger.info(f"Response: {response}")
            time.sleep(1)

            uart.send_int("3")
            response = uart.receive_int()
            if response:
                logger.info(f"Response: {response}")
            time.sleep(1)

    except KeyboardInterrupt:
        logger.exception("Exiting program.")
    finally:
        uart.close()
