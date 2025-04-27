"""This module is designed to clean user's input in general.
   Author: William Hui Chang
   Date: Wed Apr  9 00:38:19 2025
"""

import random as rd_config
import time as tm_config
import pandas as pd


# shorten data for testing on my own PC
# DATA_FILE = r"D:\DS\Py code\Crash_Analysis_System_(CAS)_data_shorten.csv"

# full data for testing on my own PC
# DATA_FILE = r"D:\DS\Py code\Crash_Analysis_System_(CAS)_data.csv"

# path directory for git commit
DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"

# DIVIDER visually divides the IDE
DIVIDER = "-" * 65

# LST_DISPLAY_LIMIT decides how many items in a list to print
LST_DISPLAY_LIMIT = 100

# PAUSE_TIME decides how long to wait
PAUSE_TIME = 1


def df_loaded_from_file(filename: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    print("Now loading ...\n...")
    ready_df = pd.read_csv(filename)
    print("Dataframe has been successfully loaded!")
    return ready_df


if __name__ == "__main__":
    # DIVIDER visually divides the IDE
    print(DIVIDER)
    print("This is what divider does.")
    print(DIVIDER)
    print()

    # LST_DISPLAY_LIMIT decides how many items in a list to print
    def print_limited_list(lst: list, limit: int) -> None:
        """ Prints a limited number of list items, hides the rest."""
        if len(lst) > limit:
            print(lst[:limit])
            print(f"\n{len(lst)} options in total. \n{limit} shown.\n")
        else:
            print(lst)
    print_limited_list([rd_config.randint(1, 100) for _ in range(50)], LST_DISPLAY_LIMIT)
    print()

    # PAUSE_TIME decides how long to wait
    def pause_a_bit() -> None:
        """ Pause a bit so that user could react. """
        tm_config.sleep(PAUSE_TIME)
    pause_a_bit()