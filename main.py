import random
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.led_matrix.device import max7219
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import tm1637
import csv
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-d","--debug", action='store_true')
args = argparser.parse_args()

def fout_controle(light_list):
    check_total = 0
    for x in range(len(light_list)):
        check_list = light_list[x]
        for y in range(len(light_list)):
            if check_list[y]:
                check_total += 1
    if check_total == 64 or check_total == 0:
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

    
def create_solver_string(light_list):
    solver_str = ""
    for x in range(len(light_list)):
        solver_str_x = ""
        for y in range(len(light_list)):
            solver_str_x += "0" if light_list[y][x] else "1"
        solver_str += solver_str_x[::-1]
    print(solver_str[::-1],end="\n\n")


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
    if args.debug:
        return test_list
    else:
        create_solver_string(light_list)
        return light_list

def create_text(locations: list, text_list: list) -> str:
    text = ''
    for i in locations:
        text += text_list[i]
    return text

def main():
    device = init_hardware()
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
    flits_time = 0.4
    button_sleep = 0.3
    while True:
        amount_of_presses = 0
        amount_of_button_presses = 0
        minutes = 0
        seconds = 0
        x_coordinaat = 0
        y_coordinaat = 0
        light_list = create_random_list()
        flits_original_state = light_list[x_coordinaat][y_coordinaat]
        load_display(light_list, device)
        time_list = []
        next_now = time.time() + flits_time
        old_time = time.time()
        old_timer = int(time.time())
        saved_value = light_list[y_coordinaat][x_coordinaat]
        start_text = "press select to start ".upper()
        start_text = list(start_text)
        try:
            delay = 0.5
            locations = [0,1,2,3]
            location_1 = 0
            location_2 = 1
            location_3 = 2
            location_4 = 3
            start_timer = time.time()
            tm.show(create_text(locations, start_text))
            while True:
                start_timer_delay = start_timer + delay
                if start_timer_delay < time.time():
                    start_timer = time.time()
                    for i in range(len(locations)):
                        locations[i] += 1
                    for i in range(len(locations)):
                        if locations[i] >= len(start_text):
                            locations[i] = 0
                    tm.show(create_text(locations, start_text))
                if GPIO.input(16) == GPIO.HIGH:#select
                    tm.show("WAIT")
                    time.sleep(0.2)
                    break
            for i in range(89):
                for halfstep in range(4):
                    for pin in range(4):
                        GPIO.output(control_pins[pin], backwards_seq[halfstep][pin])
                    time.sleep(0.005)
            while True:
                now = time.time()
                timer = int(time.time())
                if old_timer < timer:
                    # print("test")
                    time_list.append(time.time()-old_timer)
                    old_timer = int(time.time())
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
                if GPIO.input(20) == GPIO.HIGH:#left
                    light_list[y_coordinaat][x_coordinaat] = saved_value
                    x_coordinaat -= 1
                    if(x_coordinaat == -1):
                        x_coordinaat = 7
                    load_display(light_list, device)
                    saved_value = light_list[y_coordinaat][x_coordinaat]
                    time.sleep(button_sleep)
                    
                if GPIO.input(19) == GPIO.HIGH:#right
                    light_list[y_coordinaat][x_coordinaat] = saved_value
                    x_coordinaat += 1
                    if(x_coordinaat == 8):
                        x_coordinaat = 0
                    load_display(light_list, device)
                    saved_value = light_list[y_coordinaat][x_coordinaat]
                    time.sleep(button_sleep)
                    
                if GPIO.input(16) == GPIO.HIGH:#select       
                    amount_of_presses += 1
                    light_list[y_coordinaat][x_coordinaat] = saved_value
                    light_list = toggle_lights(light_list, y_coordinaat, x_coordinaat)
                    load_display(light_list, device)
                    saved_value = light_list[y_coordinaat][x_coordinaat]
                    create_solver_string(light_list)
                    time.sleep(button_sleep)
                    
                if GPIO.input(21) == GPIO.HIGH:#left
                    light_list[y_coordinaat][x_coordinaat] = saved_value
                    y_coordinaat -= 1
                    if(y_coordinaat == -1):
                        y_coordinaat = 7
                    load_display(light_list, device)
                    saved_value = light_list[y_coordinaat][x_coordinaat]
                    time.sleep(button_sleep)
                    
                if GPIO.input(26) == GPIO.HIGH:#down
                    light_list[y_coordinaat][x_coordinaat] = saved_value
                    y_coordinaat += 1
                    if(y_coordinaat == 8):
                        y_coordinaat = 0
                    load_display(light_list, device)
                    saved_value = light_list[y_coordinaat][x_coordinaat]
                    time.sleep(button_sleep)
                
                if (fout_controle(light_list)):
                    break
                
        except KeyboardInterrupt:
            device.clear()
            tm.show("    ")
            for i in range(89):
                for halfstep in range(4):
                    for pin in range(4):
                        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                    time.sleep(0.005)
        else:
            tm.show("    ")
            tm.show("WIN")
            for i in range(89):
                for halfstep in range(4):
                    for pin in range(4):
                        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                    time.sleep(0.005)
            tm.scroll("YOU WON", delay=250)
            start_text = "SAVE SCORE ".upper()
            start_text = list(start_text)
            delay = 0.5
            locations = [0,1,2,3]
            start_timer = time.time()
            tm.show(create_text(locations, start_text))
            while True:
                start_timer_delay = start_timer + delay
                if start_timer_delay < time.time():
                    start_timer = time.time()
                    for i in range(len(locations)):
                        locations[i] += 1
                    for i in range(len(locations)):
                        if locations[i] >= len(start_text):
                            locations[i] = 0
                    tm.show(create_text(locations, start_text))
                if GPIO.input(16) == GPIO.HIGH:#select
                    tm.show("WAIT")
                    with open("scores.csv", "a", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([minutes,seconds,amount_of_presses])
                    time.sleep(0.2)
                    break
                elif GPIO.input(20) == GPIO.HIGH or GPIO.input(19) == GPIO.HIGH or GPIO.input(21) == GPIO.HIGH or GPIO.input(26) == GPIO.HIGH:
                    break
        
GPIO.cleanup()

main()
