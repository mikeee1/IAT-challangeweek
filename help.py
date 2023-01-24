from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from time import sleep

serial = spi(port=0, device=0, gpio=noop(), block_orientation=-90)
device = max7219(serial, width=8, height=8)

while True:
    with canvas(device) as draw:
        draw.point((1, 1), fill="white")
    # sleep(10)