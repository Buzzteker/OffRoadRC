from machine import Pin, PWM
import utime

class Steering:
    
    def __init__(self):
        self.servo = PWM(Pin(14))
        self.servo.freq(50)
        self.Mode="sport"
        self.Target_Angle=50
        self.Last_Steer_Time=utime.ticks_ms()
        self.Current_angle=50
        
    def Set_Angle(self,angle):
        min_duty = 1638
        max_duty = 8192
        duty = int(min_duty + (angle / 100) * (max_duty - min_duty))
        self.servo.duty_u16(duty)
        
    def Update_Steering(self,Angle,Mode):
        now= utime.ticks_ms()
        Settings=Mode
        Delay=Settings["Delay"]
        Step=Settings["Step"]
        Maximum=Settings["Maximum_Angle"]
        Minimum=Settings["Minimum_Angle"]

        if Angle>Maximum:
            self.Target_Angle=Maximum
        elif Angle<Minimum:
            self.Target_Angle=Minimum
        else:
            self.Target_Angle=Angle

        if utime.ticks_diff(now,self.Last_Steer_Time)>=Delay:
            if self.Current_angle < self.Target_Angle:
                self.Current_angle=min(self.Current_angle + Step, self.Target_Angle)
            elif self.Current_angle > self.Target_Angle:
                self.Current_angle = int(max(self.Current_angle - Step, self.Target_Angle))
            
            self.Set_Angle(self.Current_angle)
            self.Last_Steer_Time=now
 


    