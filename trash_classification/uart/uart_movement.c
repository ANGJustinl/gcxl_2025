#include <REGX52.H>

// 声明舵机相关变量
int angle; // 舵机角度
int to_angle; // 目标角度

sbit DJ = P0^0; // 舵机控制信号
sbit KEY1 = P0^1;
sbit KEY2 = P0^2;
sbit KEY3 = P0^3;
sbit KEY4 = P0^4;

// Uart 相关函数声明
void uart_init();
void uart_send(char data);
char uart_receive();
int num_uart_receive();

// 舵机相关函数声明
void Servo_Init();
void Servo_Turn(int to_angle);

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


// 初始化舵机及相关设置
void Servo_Init() {
    TMOD = 0x01; // 定时器0模式1
    TL0 = 0x33;  // 定时器初值
    TH0 = 0xFE;
    TR0 = 1;     // 启动定时器
    ET0 = 1;     // 启用定时器0中断
    EA = 1;      // 开启总中断
}

void Servo_Turn(int to_angle) {
    if (to_angle > 3) { angle = 3; }
    else if (to_angle < 1) { angle = 1; }
    else { angle = to_angle; }
}

void T0isr() interrupt 1 {
    uint count;
    TL0 = 0x33;
    TH0 = 0xFE;
    count++;
    if (count <= angle) DJ = 1;
    if (count > angle && count <= 40) DJ = 0;
    if (count > 40) count = 0;
}

// 延时函数
void Delay(unsigned int xms) {
    while (xms--) {
        unsigned char i, j;
        i = 2;
        j = 239;
        do {
            while (--j);
        } while (--i);
    }
}

void main() {
    UART_Init(); // 初始化串口
    Servo_Init(); // 初始化舵机
    angle = 2;   // 设置初始角度

    while (1) {
        uart_send(angle + '0'); // 发送当前角度
        Servo_Turn(num_uart_receive()); // 根据接收到的旋转次数控制舵机
        Delay(500); // 延时以防止频繁操作
    }
}