# -*- coding: utf-8 -*-
"""This program is designed to cleanse data, organize, identify trends and
visualize data for ill-specified, complex data-science problems.
   Author: William Hui Chang
   Date: Fri Mar 21 21:06:21 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import time
import random

# shorten data for test
# DATA_FILE = r"D:\DS\Py code\Crash_Analysis_System_(CAS)_data_shorten.csv"
DATA_FILE = r"D:\DS\Py code\Crash_Analysis_System_(CAS)_data.csv"

# original data
# DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"
DIVIDER = "-" * 65
LST_DISPLAY_LIMIT = 100
PAUSE_TIME = 1
MENU = [
    "Make sure to read the dataframe first",
    "Search for related columns based on keyword",
    "Check for unique column variables of a specific column",
    "Crash Severity Report",
    "all years: Crash Severity Report", 
    "Crash Reports Over Time Graph",
    "Vehicle Types and Crash Severity Graphing",
    "Cross-Sectional Sampling",
    "Sampling Based On Interpretation",
    "Exit"
]


def pause_a_bit() -> None:
    """ Pause a bit so that user could react. """
    time.sleep(PAUSE_TIME)


def is_numeric(dirty_data: str) -> bool:
    """Check if a given string can be converted to a numeric value."""
    try:
        int(float(dirty_data.strip()))
        return True
    except (ValueError, TypeError):
        return False


def raw_format(user_input: str) -> str:
    """ Every input should be formatted, this just leaves it there. """
    return user_input


def general_format(user_input: str) -> str:
    """Returns a stripped, lower case standardized string."""
    if is_numeric(user_input):
        return user_input.strip()
    return user_input.strip().lower()


def case_sensitive_format(user_input: str) -> str:
    """Returns a stripped, case sensitive standardized string."""
    return user_input.strip()


def the_loopfather(func: callable, data: pd.DataFrame, format_func: callable) -> None:
    """User will continue using the same function unless they say 'no'."""
    user_stays = "yes by default"
    while user_stays != "no":
        func(data, format_func)
        user_stays = format_func(input(rand_msg("leave prompt")))
    print(rand_msg("bye msg"))


def rand_msg(msg_variant: str) -> str:
    """ I'm just bored. """
    option_headers = [
    "Here’s what we’ve got for you:\n",
    "Pick your poison (or pleasure):\n",
    "Take your pick from the menu below:\n"
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
    bye_msgs = [
    "That’s a wrap, thanks for hanging out!",
    "Session ended, see you next time!",
    "All done for now, take care and crunch on!"
    ]
    if msg_variant == "input prompt":
        return random.choice(input_prompts)
    elif msg_variant == "leave prompt":
        return random.choice(leave_prompts)
    elif msg_variant == "option header":
        return random.choice(option_headers)
    elif msg_variant == "success msg":
        return random.choice(success_msgs)
    elif msg_variant == "error msg":
        return random.choice(error_msgs)
    elif msg_variant == "bye msg":
        return random.choice(bye_msgs)


def list_index_as_strings(listed_options: list) -> list[str]:
    """Converts list indices to strings."""
    return [str(i) for i in range(len(listed_options))]


def display_indexed_options(options: list) -> None:
    """Displays listed options for users."""
    print(rand_msg("option header"))
    for index, option in enumerate(options):
        print(f"{index}: {option}")


def user_value_in_list(input_prompted_func: callable, \
                       options: list[str], \
                           format_func: callable\
                               ) -> str:
    """Returns a valid index number from the provided menu options."""
    while True:
        option = input_prompted_func(options, format_func)
        if option in options:
            print(rand_msg("success msg"))  
            break
        print(rand_msg("error msg"))
    return option


def print_column_matches(df: pd.DataFrame, format_func: callable) -> None:
    """Finds and prints column names containing the user-provided search term."""
    print("Got something you think might match a column?")
    search_term = format_func(input(rand_msg("input prompt")))
    print()
    matching_columns = [col for col in df.columns if search_term in col.lower()]
    if matching_columns == []:
        print(f'There is no column related to "{search_term}".')
    else:
        print("Related column name(s) listed below: ")
        print(matching_columns)
    print(DIVIDER)


def menu_choice_prompted(options: list, format_func: callable) -> str:
    """ Displays menu, and prompt the user to type. """
    print(DIVIDER)
    print("Menu")
    display_indexed_options(MENU)
    print(DIVIDER)
    print(f"User options: 0 - {len(options) - 1}")
    user_index = format_func(input(rand_msg("input prompt")))
    return user_index


def end_of_application() -> bool:
    """Ends the application."""
    print(rand_msg("bye msg"))
    return True


def df_loaded_from_file(file: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    print("Now loading ...\n...")
    ready_df = pd.read_csv(file)
    print("Dataframe has been already loaded!")
    return ready_df


def df_not_loaded(df: pd.DataFrame) -> bool:
    """ Returns True if the dataframe is not yet loaded. """
    if df is None:
        print("The dataframe hasn't been loaded yet.")
        print("Please load the data first (option 0) in the Menu.")
        pause_a_bit()
        return True
    return False


def list_without_duplicates(lst: list) -> list:
    """ Returns unique values from a list to a new list. """
    return list(set(lst))


def print_column_levels(df: pd.DataFrame, format_func: callable) -> None:
    """Prints the unique levels of a user-specified column."""
    valid_col = user_value_in_list(input_prompted, list(df.columns), format_func)
    print("\nUnique column values as below.")
    print(list(df[valid_col].unique()))
    print(DIVIDER)


def input_prompted(lst: list, format_func: callable) -> str:
    """ Displays choices, and prompt the user to type. """
    print_limited_list(lst, LST_DISPLAY_LIMIT)
    user_text = format_func(input(rand_msg("input prompt")))
    return user_text


def print_limited_list(lst: list, limit: int) -> None:
    """Prints a limited number of list items, hides the rest."""
    if len(lst) > limit:
        print(lst[:limit])
        print(f"\n{len(lst)} options in total. \n{limit} shown.\n")
    else:
        print(lst)


def plot_crashes_over_time(df: pd.DataFrame, \
                           year_start: int, \
                               year_end: int, \
                                   severities: list) -> None:
    """ Plots a multi-line graph of crash counts over time, 
    filtered by year range and crash severity types.
    """
    # filter data
    filtered_df = df[
        (df["crashYear"] >= year_start) &
        (df["crashYear"] <= year_end) &
        (df["crashSeverity"].isin(severities))
    ]
    # group and pivot data
    counts = filtered_df.groupby(['crashYear', 'crashSeverity'])\
                        .size()\
                        .unstack(fill_value=0)
    # plot
    counts.plot(kind='line', marker='o', figsize=(10, 6))
    plt.title("Crash Reports Over Time by Severity")
    plt.xlabel("Year")
    plt.ylabel("Number of Crashes")
    plt.legend(title="Crash Severity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def plot_multi_line():
    """ Plots a multi line graph based on given df and conditions. """
    pass


def main() -> None:
    """Small application that presents tables and graphs based on crash data."""
    terminate = None
    raw_df = None
    while terminate != True:
        selection = int(user_value_in_list(menu_choice_prompted, \
                                           list_index_as_strings(MENU), \
                                           general_format))
        match MENU[selection]:
            case "Exit":
                terminate = end_of_application()
            case "Make sure to read the dataframe first":
                raw_df = df_loaded_from_file(DATA_FILE)
            case "Search for related columns based on keyword":
                if df_not_loaded(raw_df):
                    continue
                the_loopfather(print_column_matches, raw_df, general_format)
            case "Check for unique column variables of a specific column":
                if df_not_loaded(raw_df):
                    continue
                the_loopfather(print_column_levels, raw_df, case_sensitive_format)
            case "Crash Severity Report":
                if df_not_loaded(raw_df):
                    continue
                print("under construction~")
                # the_loopfather(print_crash_severity_report, raw_df, general_format)
                print("under construction~")
                # the_loopfather(print_crash_severity_report, raw_df, general_format)
            case "all years: Crash Severity Report":
                if df_not_loaded(raw_df):
                    continue
                
            case "Crash Reports Over Time Graph":
                if df_not_loaded(raw_df):
                    continue
                # the_loopfather(plot_crashes_over_time, raw_df, general_format)
                crash_years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2015, 2014, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
                start_of_interest = 2000
                end_of_interest = 2015
                if start_of_interest in crash_years and start_of_interest in crash_years and start_of_interest <= end_of_interest:
                    start_selection = start_of_interest
                    end_selection = end_of_interest
                plot_crashes_over_time(raw_df, start_selection, end_selection, ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"])
            case "Vehicle Types and Crash Severity Graphing":
                pass
            case "Cross-Sectional Sampling":
                pass
            case "Sampling Based On Interpretation":
                pass
        pause_a_bit()


# use while loop in main, so that i can stay in the function
# dont loop loading data every main loop, to avoid data loading laggy as well
# each case will have a sub loop til quit, with the 1st argument as the main function, 
    # and other open **arg as necessary standards and materials and helper functions
# procedure function get the work done, other functions offer outputs as input for procedures
# global variables are raw values, other variables are just formulated links
# each case has this pattern:
    # initial information display
    # prompt for input
    # validation of input
    # use input as condition to do something


main()
