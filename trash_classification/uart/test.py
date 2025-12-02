import serial
import time

# 配置串口
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600             # 波特率设置
DATA_BITS = 8                # 数据位
STOP_BITS = 1                # 停止位
PARITY = 'N'                 # 无校验位

def main():
    try:
        # 打开串口
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # 超时时间
        )
        
        # 确保串口打开成功
        if not ser.is_open:
            ser.open()

        print(f"Serial port {SERIAL_PORT} opened with baud rate {BAUD_RATE}")

        # 定义循环发送数字 0-9
        while True:
            for i in range(10):
                # 发送数字
                ser.write(str(i).encode('utf-8'))  # 编码为字节发送
                print(f"Sent: {i}")

                # 尝试接收回显
                time.sleep(0.1)  # 等待数据返回
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    print(f"Received: {response}")

                time.sleep(1)  # 间隔发送下一数字

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        if ser and ser.is_open:
            ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
