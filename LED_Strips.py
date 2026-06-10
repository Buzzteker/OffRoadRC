from machine import Pin
import neopixel
import utime
import SBUS
print(SBUS.channels[2])

class LEDs:
    def __init__(self):
        self.NUM_LEDS = 8
        self.DATA_PIN = 18
        self.strip = neopixel.NeoPixel(Pin(self.DATA_PIN), self.NUM_LEDS)
        self.Last_Update=utime.ticks_ms()
        self.count=0
    def Send_Data(self,Red,Green,Blue):
        now=utime.ticks_ms()

        if utime.ticks_diff(now,self.Last_Update)>20:
            if self.count >= self.NUM_LEDS:
                self.count=0
            self.strip[self.count] = (Red, Green, Blue)
            self.Last_Update=now
            self.strip.write()
            self.count=self.count+1
            
            
#             
# led=LEDs()
# 
# 
# while True:
#     SBUS.update()
#     print(SBUS.channels[2])
#     L=100-SBUS.channels[5]
#     led.Send_Data(int(SBUS.channels[2]*2.55),int(L*2.25),0)
#     utime.sleep_ms(10)