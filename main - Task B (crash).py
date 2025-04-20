# -*- coding: utf-8 -*-
"""This program is designed to cleanse data, organize, identify trends and
visualize data for ill-specified, complex data-science problems.
   Author: William Hui Chang
   Date: Fri Mar 21 21:06:21 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
from config_module import DATA_FILE
from menu_module import Menu


def df_loaded_from_file(file: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    print("Now loading ...\n...")
    ready_df = pd.read_csv(file)
    print("Dataframe has been successfully loaded!")
    return ready_df

# Load dataset
df = df_loaded_from_file(DATA_FILE)



###### part 2 features consideration ######
# feature 1, validate input done
def test_invalid_year_speed_input():
    year_test = pd.DataFrame({"crashYear": [
        2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 
        2008, 2009, 2010, 2011, 2012, 2013, 2015, 2014, 
        2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]})
    speed_test = pd.DataFrame({"speedLimit": [
        70.0, 100.0, 50.0, 80.0, 60.0, 30.0, 20.0, 40.0, 
        10.0, 90.0, float('nan'), 110.0, 15.0, 5.0, 61.0, 
        6.0, 51.0, 2.0]})
    selected_year = None
    selected_speed = None
    while selected_year == None:
        selected_year = Menu(year_test["crashYear"]).display_with_values().general_prompt().validate_with_values()
    while selected_speed == None:
        selected_speed = Menu(speed_test["speedLimit"]).display_with_values().general_prompt().validate_with_values()


# feature 2, crash report with temporarySpeedLimit done
def crash_report():
    #  report <- df %>% mutate %>% select %>% filter %>% group_by %>% summurize
    # "index == index" for all condition in query()
    # "crashSeverity in ['Non-Injury Crash', 'Fatal Crash']" for multiple levels count
    report = df \
    .assign(effectiveSpeedLimit = 
            lambda df: df['temporarySpeedLimit'].combine_first(df['speedLimit'])) \
    .loc[:, ['crashSeverity', 'crashYear', 'effectiveSpeedLimit']] \
    .query("index == index") \
    .groupby('crashSeverity') \
    .size() \
    .reset_index(name='count') \
    .to_string(index=False)
    print(report)


# feature 3, no report found warning
def prompt_year_with_no_crash_warning():
    #  report <- df %>% mutate %>% select %>% filter %>% group_by %>% summurize
    # **{} for default placeholder in assign()
    crashes_on_severity = df \
        .assign(**{}) \
        .loc[:, ['crashYear', 'crashSeverity']] \
        .query("crashSeverity in ['Fatal Crash', 'Serious Crash', 'Minor Crash', 'Non-Injury Crash']") \
        .groupby(['crashYear', 'crashSeverity']) \
        .size() \
        .unstack(fill_value=0)  # crashSeverity becomes columns
    print(crashes_on_severity)
    print()
    # just let crash_number = 0 when searching for zero crash years for any_crash_type
    # here i use 300 instead to demonstrate
    any_crash_type = ["Fatal Crash"]
    crash_number = 300
    # zero_crash_years = crashes_on_severity[(crashes_on_severity[any_crash_type] <= crash_number).any(axis=1)].index.tolist()
    # print()
    years_with_crashes = crashes_on_severity[(crashes_on_severity[any_crash_type] > crash_number).any(axis=1)].index.tolist()
    valid_crash_year = None
    while valid_crash_year == None:
        print(f"Years as below that exist more than {crash_number} crashes: \n{years_with_crashes}")
        valid_crash_year = Menu(years_with_crashes).general_prompt().validate_with_values()
        if valid_crash_year == None:
            print(f"No crash record exists for your input")
            Menu.rand_msg("error msg")
    return valid_crash_year


# feature 4, all years - Crash Severity Report
def all_year_crash_report():
    #  report <- df %>% mutate %>% select %>% filter %>% group_by %>% summurize
    # "index == index" for all condition in query()
    report = df \
    .assign(effectiveSpeedLimit = 
            lambda df: df['temporarySpeedLimit'].combine_first(df['speedLimit'])) \
    .loc[:, ['crashSeverity', 'crashYear', 'effectiveSpeedLimit']] \
    .query("crashSeverity in ['Non-Injury Crash', 'Fatal Crash']") \
    .groupby('crashSeverity') \
    .size() \
    .reset_index(name='count') \
    .to_string(index=False)
    print(report)


# feature 5, 
def plot_crash_trends():
    report = df \
        .assign(**{}) \
        .loc[:, ['crashYear', 'crashSeverity']] \
        .query("crashSeverity in ['Fatal Crash', 'Serious Crash', 'Minor Crash']") \
        .groupby(['crashYear', 'crashSeverity']) \
        .size() \
        .unstack(fill_value=0)  # crashSeverity becomes columns

    # plot each severity as a line
    report.plot(kind='line', marker='o')

    plt.title("Crash Trends by Year")
    plt.xlabel("Crash Year")
    plt.ylabel("Number of Crashes")
    plt.grid(True)
    plt.tight_layout()
    plt.legend(title='Crash Severity')
    plt.show()



print()

# feature 1
print("Feature 1 as below:")
test_invalid_year_speed_input()
print()


# feature 2
print("Feature 2 as below:")
crash_report()
print()

# feature 3
print("Feature 3 as below:")
prompt_year_with_no_crash_warning()
print()

# feature 4
print("Feature 4 as below:")
all_year_crash_report()
print()

# feature 5
print("Feature 5 as graph:")
plot_crash_trends()