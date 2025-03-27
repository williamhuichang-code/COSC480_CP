# -*- coding: utf-8 -*-
"""This program is designed to cleanse data, organize, identify trends and
visualize data for ill-specified, complex data-science problems.
   Author: William Hui Chang
   Date: Fri Mar 21 21:06:21 2025
"""

import pandas as pd
import time
from typing import Callable, List, Union
import random

# shorten data for test
# DATA_FILE = r"D:\DS\Py code\Crash_Analysis_System_(CAS)_data_shorten.csv"

# original data
DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"
DIVIDER = "-" * 65
MENU = [
    "Make sure to read the dataframe first",
    "Search for related columns based on keyword",
    "Check for unique column variables of a specific column",
    "Crash Severity Report",
    "Crash Reports Over Time Graph",
    "Vehicle Types and Crash Severity Graphing",
    "Cross-Sectional Sampling",
    "Sampling Based On Interpretation",
    "Exit"
]


def the_loopfather(func: Callable, data: pd.DataFrame) -> None:
    """User will continue using the same function unless they say 'no'."""
    user_stays = "yes by default"
    while user_stays != "no":
        func(data)
        user_stays = cleaned_text_input(input(rand_msg("leave prompt")))
    print("Goodbye!")


def rand_msg(msg_variant: str) -> str:
    """ I'm just bored. """
    input_prompts = [
    "Go ahead, type your choice: ",
    "Your turn! Write something? ",
    "Make your pick and hit Enter: "
    ]
    leave_prompts = [
    "Press Enter to continue exploring, \nor type 'no' to exit the loop: ",
    "Still in the zone? Hit Enter to keep going, \nor 'no' to break free: ",
    "Ready for another round? Just press Enter, \nor type 'no' to stop: "
    ]
    if msg_variant == "input prompt":
        return random.choice(input_prompts)
    elif msg_variant == "leave prompt":
        return random.choice(leave_prompts)



def cleaned_text_input(user_input: str) -> str:
    """Returns a stripped, lower case standardized string."""
    return user_input.strip().lower()


def cleaned_numeric_input(user_input: str) -> str:
    """Returns a stripped version of the numeric string."""
    return user_input.strip()


def is_numeric(dirty_data: str) -> bool:
    """Check if a given string can be converted to a numeric value."""
    try:
        int(float(dirty_data))
        return True
    except (ValueError, TypeError):
        return False


def levels_of_a_column(col: str, df: pd.DataFrame) -> List:
    """Returns unique values of a given column."""
    return list(df[col].unique())


def nlevels_of_a_column(col: str, df: pd.DataFrame) -> int:
    """Returns number of unique values in a given column."""
    return len(list(df[col].unique()))


def print_limited_list(lst: List, limit: int) -> None:
    """Prints a limited number of list items, hides the rest."""
    if len(lst) > limit:
        print(lst[:limit] + ["..."], ", more values are hidden. ")
    else:
        print(lst)


def list_without_nan(dirty_list: List) -> List:
    """Removes NaN values from the list."""
    fresh_list = [value for value in dirty_list if not pd.isna(value)]
    return fresh_list


def display_menu(options: List[str]) -> None:
    """Displays menu options for users."""
    print(DIVIDER)
    print("Options as below:\n")
    for index, option in enumerate(options):
        print(f"{index}: {option}")
    print(DIVIDER)


def validated_index_choice(listed_options: List[str]) -> int:
    """Returns a valid index number from the provided menu options."""
    valid_input_strings = index_as_strings(MENU)
    input_prompt, success_message, error_message = defined_menu_prompts(MENU)
    while True:
        user_text = cleaned_numeric_input(input(input_prompt))
        if user_text in valid_input_strings:
            print(success_message)
            print(DIVIDER)
            break
        print(error_message)
    return int(user_text)


def defined_menu_prompts(menu: List[str]) -> tuple:
    """Defines necessary prompt messages for the menu interface."""
    menu_input_prompt = f"User options: 0 - {len(menu) - 1} \nEnter the option number and press ENTER: "
    menu_success_message = "Here you go!"
    menu_error_message = f"Invalid input. Please enter a number from 0 to {len(menu) - 1}.\n"
    return menu_input_prompt, menu_success_message, menu_error_message


def index_as_strings(listed_options: List[str]) -> List[str]:
    """Converts list indices to strings for validation purposes."""
    return [str(i) for i in range(len(listed_options))]


def end_of_application() -> bool:
    """Ends the application."""
    print("See you around!")
    return True


def df_loaded_from_file(file: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    print("Loading the data frame...")
    return pd.read_csv(file)


def find_column_matches(df: pd.DataFrame) -> None:
    """Finds and prints column names containing the user-provided search term."""
    search_term = cleaned_text_input(input("Please type the search term: "))
    matching_columns = [col for col in df.columns if search_term in col.lower()]
    if matching_columns == []:
        print("Related column name(s) listed below: ")
        print(f'There is no column related to "{search_term}".')
    else:
        print(matching_columns)
    print()


def show_column_levels(df: pd.DataFrame) -> None:
    """Prints the unique levels of a user-specified column."""
    user_stays = "yes by default"
    while user_stays != "no":
        user_choice = input("Please type the column name: ").strip()
        if user_choice in df.columns:
            unique_values = levels_of_a_column(user_choice, df)
            n_unique_values = nlevels_of_a_column(user_choice, df)
            print_limited_list(unique_values, 100)
            print(f"There are {n_unique_values} different unique values out of {len(df[user_choice])} in column {user_choice} .")
            print()
        else:
            print(f'There is no such column name as "{user_choice}" in the dataframe.')
            print()
        print("Wanna show levels for some other columns? ")
        user_stays = cleaned_text_input(input('Enter to continue, type "no" to leave: '))
    print("Goodbye!")


def print_crash_severity_report(year_of_interest: int, speed_of_interest: int, data: pd.DataFrame) -> None:
    """Prints a table outlining the number of crashes in a given year for a given speed limit."""
    crash_dataframe = data.loc[:, ["crashYear", "speedLimit", "temporarySpeedLimit", "crashSeverity"]][:]
    crash_dataframe["effectiveSpeedLimit"] = crash_dataframe.apply(
        lambda row: row["temporarySpeedLimit"] if is_numeric(row["temporarySpeedLimit"]) else row["speedLimit"],
        axis=1)
    severity_types = levels_of_a_column("crashSeverity", crash_dataframe)
    print("Crash Severity by Classification")
    print(f"Speed: {speed_of_interest}")
    print(f"Year: {year_of_interest}")
    print()
    for severity_type in severity_types:
        count = 0
        for row in crash_dataframe.itertuples(index=False):
            year = row.crashYear
            speed_limit = row.effectiveSpeedLimit
            crash_type = row.crashSeverity
            if year == year_of_interest and speed_limit == speed_of_interest and crash_type == severity_type:
                count += 1
        print(f"{severity_type}: {count}")


def is_crash_input_valid(user_text: str, constraint: List) -> bool:
    """Validates user input for year or speed against constraints."""
    standardized_text = cleaned_numeric_input(user_text)
    is_intended_numberic = is_numeric(standardized_text)
    is_in_valid_range = False
    cleaned_constraint = list_without_nan(constraint)
    for value in cleaned_constraint:
        try:
            if str(int(value)) == standardized_text or str(float(value)) == standardized_text:
                is_in_valid_range = True
        except (ValueError, TypeError):
            continue
    return is_intended_numberic and is_in_valid_range


def validated_crash_selection(constraint: List) -> str:
    """Prompts user until valid input is provided; returns cleaned selection."""
    valid = None
    while valid != True:
        print("Choices as below: ")
        print(constraint)
        user_text = input("Choose a value: ")
        valid = is_crash_input_valid(user_text, constraint)
        if valid == False:
            print("Not valid, maybe try again.")
    selection = cleaned_numeric_input(user_text)
    return selection


def main() -> None:
    """Small application that presents tables and graphs based on crash data."""
    terminate = None
    while terminate != True:
        display_menu(MENU)
        selection = validated_index_choice(MENU)
        match MENU[selection]:
            case "Exit":
                terminate = end_of_application()
            case "Make sure to read the dataframe first":
                original_dataframe = df_loaded_from_file(DATA_FILE)
                print("Dataframe has been successfully loaded! \nPlease go ahead.")
            case "Search for related columns based on keyword":
                the_loopfather(find_column_matches, original_dataframe)
            case "Check for unique column variables of a specific column":
                show_column_levels(original_dataframe)
            case "Crash Severity Report":
                crash_dataframe = original_dataframe.loc[:, ["crashYear", "speedLimit", "temporarySpeedLimit", "crashSeverity"]][:]
                crash_dataframe["effectiveSpeedLimit"] = crash_dataframe.apply(
                    lambda row: row["temporarySpeedLimit"] if is_numeric(row["temporarySpeedLimit"]) else row["speedLimit"],
                    axis=1)
                year_choices = list(crash_dataframe["crashYear"].unique())
                speed_choices = list(crash_dataframe["effectiveSpeedLimit"].unique())
                print("Select a crash year.")
                user_year = validated_crash_selection(year_choices)
                print()
                print("Select a speed limit.")
                user_speed = validated_crash_selection(speed_choices)
                print_crash_severity_report(user_year, user_speed, original_dataframe)
            case "Crash Reports Over Time Graph":
                print("This part has not been implemented yet, come back later.")
            case "Vehicle Types and Crash Severity Graphing":
                pass
            case "Cross-Sectional Sampling":
                pass
            case "Sampling Based On Interpretation":
                pass
        time.sleep(1)



main()