"""This module is designed for general helper functions I use in my data science explorations.
   Author: William Hui Chang
   Date: Sat May 24 20:56:03 2025
"""

import time
from config_global import PAUSE_TIME, DIVIDER

def pause():
    time.sleep(PAUSE_TIME)

def print_divider():
    print(DIVIDER)