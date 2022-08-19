import time
from Rosmaster_Lib import Rosmaster


def set_led(sig):
    bot = Rosmaster()

    str_id = sig
    print('Signal %s detected!' % str_id)
    if str_id == "Red":
        bot.set_colorful_lamps(0xff, 128, 0, 0)
    elif str_id == "Green":
        bot.set_colorful_lamps(0xff, 0, 128, 0)

    return True

# set_led('Green')