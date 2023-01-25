import random
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.led_matrix.device import max7219
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import tm1637

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
    # GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
    GPIO.setup(19, GPIO.IN,
               pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=8, height=8)
    control_pins = [4,17,27,22]

    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
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
    
    test_list = [[False, False, True, True, True, True, True, True],
                  [False, True, True, True, True, True, True, True],
                  [True, True, True, True, True, True, True, True],
                  [True, True, True, True, True, True, True, True],
                  [True, True, True, True, True, True, True, True],
                  [True, True, True, True, True, True, True, True],
                  [True, True, True, True, True, True, True, True],
                  [True, True, True, True, True, True, True, True]]
    
    for x in range(len(light_list)):
        change_list = light_list[x]
        change_list[random.randint(0, 7)] = True
        change_list[random.randint(0, 7)] = True
        change_list[random.randint(0, 7)] = True
        change_list[random.randint(0, 7)] = True
        light_list[x] = change_list
    return test_list


def main():
    Display = tm1637.TM1637(23,24)
    tm = tm1637.TM1637(clk=23, dio=24)
    control_pins = [4,17,27,22]
    halfstep_seq = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]]
    backwards_seq = [
        [0,0,0,1],
        [0,0,1,0],
        [0,1,0,0],
        [1,0,0,0]]
    # tm.scroll("TEAM 12 IS DE BESTE", delay=250)
    minutes = 0
    seconds = 0
    # tm.numbers(minutes,seconds)
    x_coordinaat = 0
    y_coordinaat = 0
    flits_time = 0.4
    
    light_list = create_random_list()
    flits_original_state = light_list[x_coordinaat][y_coordinaat]
    device = init_hardware()
    load_display(light_list, device)
    time_list = []
    next_now = time.time() + flits_time
    old_time = time.time()
    old_timer = int(time.time())
    saved_value = light_list[y_coordinaat][x_coordinaat]
    try:
        while True:
            if GPIO.input(16) == GPIO.HIGH:#select
                tm.show("WAIT")
                time.sleep(0.2)
                break
        for i in range(178):
            for halfstep in range(4):
                for pin in range(4):
                    GPIO.output(control_pins[pin], backwards_seq[halfstep][pin])
                time.sleep(0.005)
        while True:
            # print(int(time.time()))
            now = time.time()
            timer = int(time.time())
            # print(f'Variable timer: {timer}, Type: {type(timer)}')
            # print(f'Variable old_timer: {old_timer}, Type: {type(old_timer)}')
            if old_timer < timer:
                # print("test")
                time_list.append(time.time()-old_timer)
                old_timer = int(time.time())
                # print(f'Variable timer: {timer}, Type: {type(timer)}')
                # print(f'Variable old_timer: {old_timer}, Type: {type(old_timer)}')
                seconds += 1
                if seconds > 59:
                    seconds = 0
                    minutes += 1
                if minutes == 0 and seconds == 0:
                    print("0")
                tm.numbers(minutes,seconds)
                
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
            
            if (fout_controle(light_list)):
                break
            # old_timer = int(time.time())
            
    except KeyboardInterrupt:
        device.clear()
        tm.show("    ")
        # print(time_list)
        for i in range(178):
            for halfstep in range(4):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.005)
    else:
        tm.show("    ")
        for i in range(178):
            for halfstep in range(4):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.005)
        for i in range(5):
            tm.scroll("YOU WON", delay=250)
        
GPIO.cleanup()

main()
