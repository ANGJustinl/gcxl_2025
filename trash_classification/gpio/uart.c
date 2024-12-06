#include <REGX52.H>

// 串口初始化函数
void uart_init() {
    TMOD = 0x20;  // 定时器1，工作在模式2（自动重载）
    TH1 = 0xFD;   // 设置波特率9600 (假设12MHz晶振)
    TL1 = 0xFD;
    TR1 = 1;      // 启动定时器1
    SCON = 0x50;   // 配置串口：模式1，允许接收
    REN = 1;       // 启用接收
}

// 串口发送字符函数
void uart_send(char data) {
    SBUF = data;  // 发送数据
    while (!TI);   // 等待发送完成
    TI = 0;        // 清除发送完成标志
}

// 串口接收字符函数
char uart_receive() {
    while (!RI);  // 等待接收完成
    RI = 0;       // 清除接收完成标志
    return SBUF;  // 返回接收到的数据
}

int num_uart_receive() {
    int received_num;  // 接收到的数字
    return = uart_receive() - '0';  // 将字符转换为数字
}
