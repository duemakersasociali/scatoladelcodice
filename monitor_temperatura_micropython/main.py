__author__ = 'DueMakersAsociali'
__license__ = "MIT"
__version__ = "0.1"
__status__ = "Prototype"

from pyb import ADC
from machine import Pin, I2C
from time import sleep
from math import log

import ssd1306

from ntc_3950_lut_list import *


def binary_search(item_list, item):
    first = 0
    last = len(item_list) - 1
    found = False
    while (first <= last and not found):
        mid = (first + last) // 2
        if item_list[mid] == item:
            found = True
        else:
            if item > item_list[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return mid


def get_temp_with_b_parameter_eq(res, B, T0, R0):

    Tk = 273.15
    btemp = B * (T0 + Tk) / (log(res/R0) * (T0 + Tk) + B) - Tk
    return btemp


def read_temperature(adc):
    Tstart = -30
    T0 = 25.0
    R0 = 100000.0
    B = 3950

    max_adc = 4096
    data_read = adc.read()  # read value, 0-4095
    res_value = int((46000.0 * data_read) / (max_adc - data_read))
    #temp_f = binary_search(ntc_3950_lut_list, 10 * res_value) + Tstart
    temp_f = get_temp_with_b_parameter_eq(res_value, B, T0, R0)
    return temp_f, data_read


if __name__ == "__main__":

    # i2c definition
    sda_p = Pin('X10')
    scl_p = Pin('X9')
    i2c = I2C(-1, scl=scl_p, sda=sda_p)

    # oled init
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    # analog input
    adc = ADC(Pin('X4'))

    while (True):
        oled.fill(0)
        temp, data_read = read_temperature(adc)
        temperature_out = 'Temp ' + "{0:.1f}".format(temp) + ' C'
        oled.text(temperature_out, 0, 2)
        oled.text(str(data_read), 0, 20)
        oled.show()
        sleep(0.3)

