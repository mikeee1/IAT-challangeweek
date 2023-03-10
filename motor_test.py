import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
control_pins = [4,17,27,22]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

halfstep_seq = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1],
]

for i in range(512):
    for halfstep in range(4):
        for pin in range(4):
            GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
    time.sleep(0.005)

GPIO.cleanup()