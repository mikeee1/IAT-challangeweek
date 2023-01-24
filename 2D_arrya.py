import random
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.led_matrix.device import max7219
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

def fout_controle(light_list):
    check_total = 0;
    for x in range(len(light_list)):
        check_list = light_list[x]
        for y in range(len(light_list)):
            if check_list[y]:
                check_total += 1
    if check_total == 64:
        return True
    else:
        return False


def init_hardware():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(19, GPIO.IN,
               pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=8, height=8)
    return device


def load_display(full_display_list, device):
    with canvas(device) as draw:
        for y in range(len(full_display_list)):
            display_list = full_display_list[y]
            for x in range(len(display_list)):
                if(display_list[x] == True):
                    draw.point((x, y), fill="white")
                else:
                    draw.point((x, y), fill="black")


def toggle_lights(light_list, y_coordinaat, x_coordinaat):
    y_change = [y_coordinaat + 1, y_coordinaat, y_coordinaat, y_coordinaat, y_coordinaat - 1]
    x_change = [x_coordinaat, x_coordinaat - 1, x_coordinaat, x_coordinaat + 1, x_coordinaat]

    for x in range(len(y_change)):
        if(y_change[x] != -1 and y_change[x] != 8):
            change_list = light_list[y_change[x]]
            if (x_change[x] != -1 and x_change[x] != 8):
                if(change_list[x_change[x]] == True):
                    change_list[x_change[x]] = False
                else:
                        change_list[x_change[x]] = True
            light_list[y_change[x]] = change_list

    return light_list


def flits(flits_list, y_coordinaat, x_coordinaat, device):
    change_flist_list = flits_list[y_coordinaat]
    change_flist_list[x_coordinaat] = not change_flist_list[x_coordinaat]
    flits_list[y_coordinaat] = change_flist_list
    load_display(flits_list, device)

# def set_location():
    



def create_random_list():
    light_list = [[False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False]]

    for x in range(len(light_list)):
        change_list = light_list[x]
        change_list[random.randint(0, 7)] = True
        change_list[random.randint(0, 7)] = True
        change_list[random.randint(0, 7)] = True
        change_list[random.randint(0, 7)] = True
        light_list[x] = change_list
    return light_list


def main():
    x_coordinaat = 0
    y_coordinaat = 0
    flits_time = 0.4
    
    light_list = create_random_list()
    flits_original_state = light_list[x_coordinaat][y_coordinaat]
    device = init_hardware()
    load_display(light_list, device)
    
    next_now = time.time() + flits_time
    saved_value = light_list[y_coordinaat][x_coordinaat]
    try:
        while True:
            now = time.time()
            if now >= next_now:
                next_now = time.time() + flits_time
                flits(light_list, y_coordinaat, x_coordinaat, device)
                
            if GPIO.input(19) == GPIO.HIGH:#left
                light_list[y_coordinaat][x_coordinaat] = saved_value
                x_coordinaat -= 1
                if(x_coordinaat == -1):
                    x_coordinaat = 7
                load_display(light_list, device)
                saved_value = light_list[y_coordinaat][x_coordinaat]
                time.sleep(0.2)
                
            if GPIO.input(26) == GPIO.HIGH:#right
                light_list[y_coordinaat][x_coordinaat] = saved_value
                x_coordinaat += 1
                if(x_coordinaat == 8):
                    x_coordinaat = 0
                load_display(light_list, device)
                saved_value = light_list[y_coordinaat][x_coordinaat]
                time.sleep(0.2)
                
            if GPIO.input(16) == GPIO.HIGH:#select
                light_list[y_coordinaat][x_coordinaat] = saved_value
                light_list = toggle_lights(light_list, y_coordinaat, x_coordinaat)
                load_display(light_list, device)
                saved_value = light_list[y_coordinaat][x_coordinaat]
                time.sleep(0.2)
                
            if GPIO.input(20) == GPIO.HIGH:#up
                light_list[y_coordinaat][x_coordinaat] = saved_value
                y_coordinaat -= 1
                if(y_coordinaat == -1):
                    y_coordinaat = 7
                load_display(light_list, device)
                saved_value = light_list[y_coordinaat][x_coordinaat]
                time.sleep(0.2)
                
            if GPIO.input(21) == GPIO.HIGH:#down
                light_list[y_coordinaat][x_coordinaat] = saved_value
                y_coordinaat += 1
                if(y_coordinaat == 8):
                    y_coordinaat = 0
                load_display(light_list, device)
                saved_value = light_list[y_coordinaat][x_coordinaat]
                time.sleep(0.2)
                
    except KeyboardInterrupt:
        device.clear()
        


main()
