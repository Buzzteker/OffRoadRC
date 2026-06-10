import SBUS
import utime
from Steering import Steering
from Change_Modes import Modes
from Drive import Drive_Motor
from LED_Strips import LEDs

steering=Steering()
modes=Modes()
drive=Drive_Motor()
led=LEDs()



while True:
    SBUS.update()

    # Send values to change LED strip colour
    L=100-SBUS.channels[5]
    led.Send_Data(int(SBUS.channels[2]*2.55),int(L*2.25),0)
    
    # Get current mode settings
    modes.Get_Mode_Settings(SBUS.channels[5])
    Mode_Settings=modes.Get_Mode_Settings(SBUS.channels[5])
 
    # Update Steering angle using value from channel 4
    steering.Update_Steering(SBUS.channels[3],Mode_Settings)
    
    # update Motors speed using value from Channel 3
    drive.Set_Speed(SBUS.channels[2],Mode_Settings)
    
    # Prevent from rapid looping by shuting the micro controller for 20ms
    utime.sleep_ms(20)
    