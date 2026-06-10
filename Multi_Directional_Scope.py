from machine import I2C, Pin
import utime
import math
from mpu6050 import MPU6050

class MDSCOPE:
    
    def __init__(self):
        self.i2c = I2C(0, sda=Pin(11), scl=Pin(12), freq=400000)
        self.mpu = MPU6050(self.i2c)     
        self.GRAVITY=9.81
        self.Last_Record=utime.ticks_ms()
        
        self.ROLL_OFFSET  = 0
        self.PITCH_OFFSET = 0
        self.AX_OFFSET = 0
        self.AY_OFFSET = 0
        self.AZ_OFFSET = 0
        
        self.pitch = 0
        self.roll = 0
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        
    def Calibrate(self):
        samples = 50
        roll_sum, pitch_sum = 0, 0
        ax_sum, ay_sum, az_sum = 0, 0, 0
        for _ in range(samples):
            ax, ay, az = self.mpu.get_accel()
            roll_sum  += math.atan2(ay, az) * 180 / math.pi
            pitch_sum += math.atan2(-ax, az) * 180 / math.pi
            ax_sum += ax * self.GRAVITY
            ay_sum += ay * self.GRAVITY
            az_sum += az * self.GRAVITY
            utime.sleep_ms(40)
        self.ROLL_OFFSET  = roll_sum  / samples
        self.PITCH_OFFSET = pitch_sum / samples
        self.AX_OFFSET = ax_sum / samples
        self.AY_OFFSET = ay_sum / samples
        self.AZ_OFFSET = az_sum / samples

        print(f"Calibration done.")
        print(f"Accel offsets X:{self.AX_OFFSET:.2f} Y:{self.AY_OFFSET:.2f} Z:{self.AZ_OFFSET:.2f} m/s²")
        print(f"Roll offset :{self.ROLL_OFFSET:.2f} Pitch offset : {self.PITCH_OFFSET:.2f}")
        print("---")
        
    def Pitch(self):
        ax, ay, az = self.mpu.get_accel()
        self.pitch = math.atan2(-ax, az) * 180 / math.pi - self.PITCH_OFFSET
        return self.pitch
    
    def Roll(self):
        ax, ay, az = self.mpu.get_accel()
        self.roll  = math.atan2(ay, az)  * 180 / math.pi - self.ROLL_OFFSET
        return self.roll
        
    def Accel(self):
        ax, ay, az = self.mpu.get_accel()
        self.accel_x = (ax * self.GRAVITY) - self.AX_OFFSET
        self.accel_y = (ay * self.GRAVITY) - self.AY_OFFSET
        self.accel_z = (az * self.GRAVITY) - self.AZ_OFFSET
        return {
            "accel_x": self.accel_x,
            "accel_y": self.accel_y,
            "accel_z": self.accel_z,
            }
            
