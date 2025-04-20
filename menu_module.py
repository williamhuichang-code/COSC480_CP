# -*- coding: utf-8 -*-
"""This module is designed to clean user's input in general.
   Author: William Hui Chang
   Date: Wed Apr  9 00:38:19 2025
"""

import pandas as pd_menu
import random as rd_menu
from clean_input_module import CleanInput
from config_module import DIVIDER


class Menu():
    """ Displays itself, prompts input and returns validated selection. """
    # class Menu is dependent on the pandas for preprocessing its input list
    def __init__(self, lst):
        """ Initializer. """
        self.total = pd_menu.Series(lst).dropna().tolist()
        self.menu = pd_menu.Series(lst).dropna().unique().tolist()
    # step 1, display menu
    def display_with_index(self):
        """Displays listed options for users."""
        print(DIVIDER)
        print(self.rand_msg("option header"))
        for index, option in enumerate(self.menu):
            print(f"{index}: {option}")
        print(DIVIDER)
        return self
    def display_with_values(self):
        print(DIVIDER)
        print(self.rand_msg("unique values"))
        print(self.menu)
        print(DIVIDER)
        return self
    # step 2, prompt input with cleanstyle
    def general_prompt(self):
        """ Universal prompt for input. """
        self.response = CleanInput(input(self.rand_msg("input prompt"))).general_style()
        return self
    def silence_prompt(self):
        """ Universal prompt for input. """
        self.response = CleanInput(input()).general_style()
        return self
    # step 3, validate input and return selection
    def validate_with_index(self):
        """ Validates with index number, not with menu contents. """
        # condition is in well defined order, just so I always know
        if self.response.replace(" ", "").isdigit() and len(self.response.split()) > 1:
            print(self.rand_msg("whitespace error"))
            return None
        elif not self.response.isdigit():
            print(self.rand_msg("non-numeric error"))
            return None
        elif int(self.response) not in range(len(self.menu)):
            print(self.rand_msg("out-of-range error"))
            return None
        else:
            print(self.rand_msg("success msg"))
            return self.menu[int(self.response)]
    def validate_with_values(self):
        """ Validates with listed values. """
        # condition is in well defined order, just so I always know
        if self.response not in self.list_items_as_strings(self.menu):
            print(self.rand_msg("no-match error"))
            return None
        else:
            print(self.rand_msg("success msg"))
            return self.response
    # static helper method are here since it's logically related
    @staticmethod
    def list_items_as_strings(lst: list) -> list[str]:
        """ Converts list items to strings. """
        string_lst = []
        for value in lst:
            if CleanInput.is_numeric(value):
                string_lst.append(str(float(str(value).strip())))
            else:
                string_lst.append(str(value).strip())
        return string_lst
    @staticmethod
    def rand_msg(msg_variant: str) -> str:
        """ I'm just bored. """
        option_headers = [
            "Here’s what we’ve got for you:\n",
            "Pick your poison (or pleasure):\n",
            "Take your pick from the menu below:\n"
            ]
        unique_values = [
            "Check these out — one of each flavor, no duplicates!",
            "Let’s crack open the variety pack:",
            "Only the special ones made the cut — here they are:"
            ]
        input_prompts = [
            "Go ahead, type your choice: ",
            "Your turn! Write something: ",
            "Make your pick and hit Enter: "
            ]
        leave_prompts = [
            "Press Enter to continue exploring, \nor type 'no' to exit the loop: ",
            "Still in the zone? Hit Enter to keep going, \nor 'no' to break free: ",
            "Ready for another round? Just press Enter, \nor type 'no' to stop: "
            ]
        success_msgs = [
            "Got it, moving on!",
            "Nicely done, let’s keep rolling!",
            "Sweet, You're all set!"
            ]
        error_msgs = [
            "Hmm... that didn’t work. Try again?\n",
            "Not quite right — give it another shot!\n",
            "Oops! That input wasn’t valid. Wanna try once more?\n"
            ]
        whitespace_errors = [
            "Your input is doing the splits. No gymnastics allowed!",
            "Too much space... this isn’t a galaxy far, far away.",
            "One value only — leave the air between them at home!"
            ]
        no_match_errors = [
            "No match exist for your request.",
            "Out of bounds — aim better ~ ",
            "No such record found — but nice imagination!"
            ]
        non_numeric_errors = [
            "Numbers only, wizard ~ ",
            "That’s not even close to a number.",
            "Digits, please. No riddles."
            ]
        bye_msgs = [
        "That’s a wrap, thanks for hanging out!",
        "Session ended, see you next time!",
        "All done for now, take care and crunch on!"
        ]
        if msg_variant == "input prompt":
            return rd_menu.choice(input_prompts)
        elif msg_variant == "leave prompt":
            return rd_menu.choice(leave_prompts)
        elif msg_variant == "option header":
            return rd_menu.choice(option_headers)
        elif msg_variant == "unique values":
            return rd_menu.choice(unique_values)
        elif msg_variant == "success msg":
            return rd_menu.choice(success_msgs)
        elif msg_variant == "error msg":
            return rd_menu.choice(error_msgs)
        elif msg_variant == "whitespace error":
            return rd_menu.choice(whitespace_errors)
        elif msg_variant == "no-match error":
            return rd_menu.choice(no_match_errors)
        elif msg_variant == "non-numeric error":
            return rd_menu.choice(non_numeric_errors)
        elif msg_variant == "bye msg":
            return rd_menu.choice(bye_msgs)



if __name__ == "__main__":
    main_or_sub = ["Make sure to read the dataframe first",
                   "Search for related columns based on keyword",
                   "Check for unique column variables of a specific column",
                   "Crash Severity Report",
                   "all years: Crash Severity Report", 
                   "Crash Reports Over Time Graph",
                   "Vehicle Types and Crash Severity Graphing",
                   "Cross-Sectional Sampling",
                   "Sampling Based On Interpretation",
                   "Exit"]
    valid_selection = Menu(main_or_sub).display_with_index().general_prompt().validate_with_index()
    print(f"you have chosen {valid_selection}")
    print()
    numeric_lst = [70.0, 100.0, 50.0, 80.0, 60.0, 30.0, 20.0, 40.0, 
                   10.0, 90.0, float('nan'), 110.0, 15.0, 5.0, 61.0, 
                   6.0, 51.0, 2.0]
    valid_numeric_selection = Menu(numeric_lst).display_with_values().general_prompt().validate_with_values()
    print(f"you have chosen {valid_numeric_selection}")
    print()