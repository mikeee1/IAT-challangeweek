import sys
import datetime
import RPi.GPIO as GPIO
import tm1637
import time

GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#CLK -> GPIO23 (Pin 16)
#Di0 -> GPIO24 (Pin 18)

Display = tm1637.TM1637(23,24)

tm = tm1637.TM1637(clk=23, dio=24)
old_now = int(time.time())
timer = 60
pressed = False
while True:
#    now = datetime.datetime.now()
    now = int(time.time())
    if GPIO.input(19) == GPIO.HIGH:
        print("hoi")
        timer = 60
        time.sleep(0.2)
    if GPIO.input(26) == GPIO.HIGH:
        timer = 60
        print("hoi2")
        time.sleep(0.2)
    if GPIO.input(16) == GPIO.HIGH:
        timer = 60
        print("hoi3")
        time.sleep(0.2)
    if GPIO.input(20) == GPIO.HIGH:
        timer = 60
        print("hoi4")
        time.sleep(0.2)
    if GPIO.input(21) == GPIO.HIGH:
        timer = 60
        print("hoi5")
        time.sleep(0.2)
    # print(now)
    if old_now != now:
        # print("second")
        timer -= 1
#    hour = now.hour
#    minute = now.minute
#    second = now.second
#    tm.numbers(hour, minute)
#    time.sleep(1)
    tm.number(timer)
    old_now = now