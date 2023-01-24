import max7219 as led
from machine import Pin, SPI
import time


device = led.matrix(cascaded=1)
device.brightness(1)

device.show_message("RASPBERRYTIPS.NL", font=proportional(CP437_FONT))

time.sleep(3)
device.flush()