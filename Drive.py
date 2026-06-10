from machine import Pin, PWM
from Change_Modes import Modes
from Multi_Directional_Scope import MDSCOPE
import SBUS
import utime

modes=Modes()
Mode_Settings=modes.Get_Mode_Settings(SBUS.channels[5])
MDscope=MDSCOPE()


class Drive_Motor:
    def __init__(self):
        self.DriveMotor=PWM(Pin(8),freq=50)
        self.Target_Speed=50
        self.Current_Speed=50
        self.Last_Motor_Time=utime.ticks_ms()
        self.neutral = int((1500/20000) * 65535)  # = 4915
        self.DriveMotor.duty_u16(self.neutral)
        utime.sleep_ms(2000)
        
    def Set_Speed(self,Speed,Mode):
        Settings=Mode
        Maximum=Settings["Max_Speed"]
        min_duty = 3276
        max_duty = 6553
        duty = int(min_duty + (Speed / 100) * (max_duty - min_duty))
        b=duty-self.neutral
        c=b*Maximum
        Final_Speed=self.neutral+c
        self.DriveMotor.duty_u16(int(Final_Speed))

    def Update_Motor(self,Speed,Mode):
        now= utime.ticks_ms()
        Settings=Mode
        Delay=Settings["Delay"]
        Step=Settings["Step"]

        self.Target_Speed=Speed
        print(max(10,Delay+(int(MDscope.Pitch())*2.5)))
        if utime.ticks_diff(now,self.Last_Motor_Time)>=max(10,(Delay+(int(MDscope.Pitch())*2.5))):
            if self.Current_Speed<self.Target_Speed:
                self.Current_Speed=min(self.Current_Speed+Step,self.Target_Speed)
            elif self.Current_Speed>self.Target_Speed:
                self.Current_Speed=max(self.Current_Speed-Step,self.Target_Speed)
                
            self.Set_Speed(self.Current_Speed,Mode)
            self.Last_Motor_Time=now
              



