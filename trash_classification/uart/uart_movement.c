#include <REGX52.H>
#define uint unsigned int
#define uchar unsigned char


// 声明舵机相关变量
int angle; // 舵机角度
int to_angle; // 目标角度
int send_int; // 发送整数
uchar send_data; // 发送数据
sbit DJ = P0^0; // 舵机控制信号
sbit KEY1 = P0^1;
sbit KEY2 = P0^2;
sbit KEY3 = P0^3;
sbit KEY4 = P0^4;

// Uart 相关函数声明
void UART_Init();
void UART_Send(uchar send_data);
void UART_SendInt(int send_int);
uchar UART_ReceiveByte();
int UART_ReceiveInt();

// 舵机相关函数声明
void Servo_Init();
void Servo_Turn(int to_angle);

// 串口初始化
void UART_Init() {
    TMOD = 0x20; // 定时器1模式2
    TH1 = 0xFD;
    TL1 = 0xFD;
    TR1 = 1;  // 启动定时器1
    SCON = 0x50; // 8位数据，1位停止位
}

// 串口发送一个字节数据
void UART_Send(uchar send_data)
{
    while (!TI); // 等待发送缓冲区空，TI标志位为1时表示可以发送数据
    TI = 0;      // 清除发送中断标志
    SBUF = send_data; // 将数据写入SBUF寄存器，开始发送
}

// 串口发送一个整数（假设传输2字节）
void UART_SendInt(int send_int)
{
    uchar low_byte = send_int & 0xFF;          // 低字节
    uchar high_byte = (send_int >> 8) & 0xFF;  // 高字节

    UART_Send(low_byte);   // 先发送低字节
    UART_Send(high_byte);  // 再发送高字节
}

// 串口接收一个字节
uchar UART_ReceiveByte()
{
    while (!RI);   // 等待数据接收完成
    RI = 0;        // 清除接收中断标志
    return SBUF;   // 读取接收到的数据并返回
}

// 串口接收一个整数（假设接收2字节数据，转换为int）
int UART_ReceiveInt()
{
    uchar low_byte, high_byte;
    int received_value;

    low_byte = UART_ReceiveByte();    // 接收低字节
    high_byte = UART_ReceiveByte();   // 接收高字节

    received_value = (high_byte << 8) | low_byte; // 组合为一个16位整数

    return received_value;
}

// 初始化舵机及相关设置
void Servo_Init()
{
    TMOD = 0x01; // 定时器0模式1
    TL0 = 0x33;  // 定时器初值
    TH0 = 0xFE;
    TR0 = 1;     // 启动定时器
    ET0 = 1;     // 启用定时器0中断
    EA = 1;      // 开启总中断
}

void Servo_Turn(int to_angle)
// 舵机转动函数
{
    if (to_angle > 3){angle=3;}
    else if (to_angle < 1){angle=1;}
    else{angle=to_angle;}
}

void T0isr() interrupt 1
{
    uint count;
    TL0=0x33;
    TH0=0xFE;
    count++;
    if(count<=angle) DJ=1;
    if(count>angle&&count<=40) DJ=0;
    if(count>40) count=0;
}

// 延时函数
void Delay(unsigned int xms)
{
    while (xms--)
    {
        unsigned char i, j;
        i = 2;
        j = 239;
        do
        {
            while (--j);
        } while (--i);
    }
}

void main() {
    UART_Init(); // 初始化串口
    Servo_Init(); // 初始化舵机
    angle = 2;   // 设置初始角度

    while (1)
    {
        UART_SendInt(angle); // 发送当前角度
        to_angle = UART_ReceiveInt(); // 从串口接收一个整数
        Servo_Turn(to_angle); // 根据接收到的旋转次数控制舵机
        Delay(500); // 延时以防止频繁操作
    }
    Delay(50000); // 延时以防止频繁操作
}