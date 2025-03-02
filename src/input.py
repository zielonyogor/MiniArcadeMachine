import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from gpiozero import Button

# input return values
NONE = 0

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

SELECT = 5
MENU = 6

STANDBY = -1


def setup():
    # Initialize the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create an ADS1115 object
    ads = ADS.ADS1115(i2c)

    global select_button
    global menu_button
    select_button = Button(19, bounce_time=0.1)
    menu_button = Button(26, bounce_time=0.1)

    # Define the analog input channels
    global y_axis
    global x_axis
    y_axis = AnalogIn(ads, ADS.P0)
    x_axis = AnalogIn(ads, ADS.P1)

    global joystick_value
    joystick_value = NONE

def update_joystick():
    global joystick_value
    is_middle = 0

    y_value = y_axis.value
    x_value = x_axis.value

    if y_value < 5_000 and joystick_value != STANDBY:
        joystick_value = UP
    elif y_value > 28_000 and joystick_value != STANDBY:
        joystick_value = DOWN
    elif 5_000 < y_value < 28_000 and joystick_value == STANDBY:
        is_middle += 1

    if x_value < 5_000 and joystick_value != STANDBY:
        joystick_value = RIGHT
    elif x_value > 28_000 and joystick_value != STANDBY:
        joystick_value = LEFT
    elif 5_000 < x_value < 28_000 and joystick_value == STANDBY:
        is_middle += 1

    if is_middle == 2:
        joystick_value = NONE

def get_joystick_input():
    global joystick_value
    if joystick_value == STANDBY or joystick_value == NONE:
        return NONE

    return_value = joystick_value
    joystick_value = STANDBY
    return return_value

def get_button_input():
    if select_button.is_pressed:
        return SELECT
    if menu_button.is_pressed:
        return MENU
    return NONE