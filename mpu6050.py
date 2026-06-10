import time
from machine import I2C

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def read_raw(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        val = (data[0] << 8) | data[1]
        if val > 32767:
            val -= 65536
        return val

    def get_accel(self):
        x = self.read_raw(0x3B) / 16384.0
        y = self.read_raw(0x3D) / 16384.0
        z = self.read_raw(0x3F) / 16384.0
        return x, y, z

    def get_gyro(self):
        x = self.read_raw(0x43) / 131.0
        y = self.read_raw(0x45) / 131.0
        z = self.read_raw(0x47) / 131.0
        return x, y, z

    def get_temp(self):
        raw = self.read_raw(0x41)
        return (raw / 340.0) + 36.53