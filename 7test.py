#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://raspberrytips.nl

import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637

#CLK -> GPIO23 (Pin 16)
#Di0 -> GPIO24 (Pin 18)

Display = tm1637.TM1637(23,24)

tm = tm1637.TM1637(clk=23, dio=24)
while True:
#    now = datetime.datetime.now()
#    hour = now.hour
#    minute = now.minute
#    second = now.second
#    tm.numbers(hour, minute)
#    time.sleep(1)
   tm.scroll("TEAM 12 IS DE BESTE", delay=250)
