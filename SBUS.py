from machine import UART, Pin
import time

uart = UART(1, baudrate=100000, rx=Pin(6),bits=8, parity=0, stop=2, invert=UART.INV_RX)

channels = [0] * 6

def find_frame(data):

    for i in range(len(data) - 25):
        if data[i] == 0x0F and data[i + 25] == 0x0F:
            return data[i:i + 25]
    return None

def parse_sbus(data):
    ch = [0] * 6
    ch[0] = (data[1] | data[2] << 8) & 0x7FF
    ch[1] = (data[2] >> 3 | data[3] << 5) & 0x7FF
    ch[2] = (data[3] >> 6 | data[4] << 2 | data[5] << 10) & 0x7FF
    ch[3] = (data[5] >> 1 | data[6] << 7) & 0x7FF
    ch[4] = (data[6] >> 4 | data[7] << 4) & 0x7FF
    ch[5] = (data[7] >> 7 | data[8] << 1 | data[9] << 9) & 0x7FF
    return ch

def sbus_to_percent(raw):
    return max(0, min(100, int((raw - 200) / 16)))

def update():
    global channels
    if uart.any() > 50:
        data = uart.read(uart.any())
        frame = find_frame(data)
        if frame:
            raw = parse_sbus(frame)
            channels = [sbus_to_percent(v) for v in raw]
        uart.read(uart.any())