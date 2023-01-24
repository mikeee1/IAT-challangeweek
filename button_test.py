import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True: # Run forever
    if GPIO.input(35) == GPIO.HIGH:
        print("Button 21 was pushed!")
        time.sleep(0.2)
    if GPIO.input(36) == GPIO.HIGH:
        print("Button 22 was pushed!")
        time.sleep(0.2)
    if GPIO.input(37) == GPIO.HIGH:
        print("Button 23 was pushed!")
        time.sleep(0.2)
    if GPIO.input(38) == GPIO.HIGH:
        print("Button 24 was pushed!")
        time.sleep(0.2)
    if GPIO.input(40) == GPIO.HIGH:
        print("Button 26 was pushed!")
        time.sleep(0.2)