#include <REGX52.H> 
#define uint unsigned int
#define uchar unsigned char

sbit DJ = P0^0;
sbit KEY1 = P0^1;
sbit KEY2 = P0^2;
sbit KEY3 = P0^3;
sbit KEY4 = P0^4;

// 更具辨识度的变量名
int rotation_angle;

// 延时函数
void Delay(unsigned int xms)
{
    while(xms--)
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

// 初始化系统状态
void init_system()
{
    TMOD = 0x01;
    TL0 = 0x33;
    TH0 = 0xFE;
    TR0 = 1;
    ET0 = 1;
    EA = 1;
    rotation_angle = 3;
}

// 更新角度值
void update_rotation_angle(int delta)
{
    rotation_angle += delta;
    if (rotation_angle < 1)
    {
        rotation_angle = 1;
    }
    else if (rotation_angle > 4)
    {
        rotation_angle = 4;
    }
}

// 外部暴露接口，用于设置角度
__declspec(dllexport) void set_rotation_angle(int angle)
{
    // 计算增量并更新
    int delta = angle - rotation_angle;
    update_rotation_angle(delta);
}

// 外部暴露接口，用于获取当前角度
__declspec(dllexport) int get_rotation_angle()
{
    return rotation_angle;
}

// 主函数
void main()
{
    init_system();
    while(1)
    {
        if(P3_1 == 0) // 按钮控制旋转的判断
        {
            Delay(10);
            if(P3_1 != 0)
            {
                update_rotation_angle(-1);
            }
        }
        if(P3_0 == 0)
        {
            Delay(10);
            if(P3_0 != 0)
            {
                update_rotation_angle(1);
            }
        }
    }
}

// 定时器 0 中断服务函数
void T0isr() interrupt 1
{
    static uint count = 0;
    TL0 = 0x33;
    TH0 = 0xFE;
    count++;
    if(count <= rotation_angle) 
        DJ = 1;
    if(count > rotation_angle && count <= 40) 
        DJ = 0;
    if(count > 40) 
        count = 0;
}
