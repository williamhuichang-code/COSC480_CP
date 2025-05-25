"""This module is for functions specific to crash report project.
   Author: William Hui Chang
   Date: Sat Apr 26 10:43:45 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
from config_global import DATA_FILE, df_loaded_from_file
from class_helper_menu import Menu


###### part 2 features consideration ######
# feature 2, crash report prioritizing temporarySpeedLimit, and using speedLimit as fallback
def df_with_effective_speed(crash_df: pd.DataFrame) -> pd.DataFrame:
   """ Return new crash df with effective speed limit. """
   new_df = crash_df.assign(effectiveSpeedLimit = 
         lambda crash_df: crash_df['temporarySpeedLimit'].combine_first(crash_df['speedLimit']))
   return new_df


# core report table for year, speed, crash severity type
def core_crash_severity_data(crash_df: pd.DataFrame) -> pd.DataFrame:
   """ Returns core dataframe for further reports and graphs. """
   core_df = df_with_effective_speed(crash_df) \
      .loc[:,['crashYear', 'effectiveSpeedLimit', 'crashSeverity']] \
      .groupby(['crashYear', 'crashSeverity', 'effectiveSpeedLimit']) \
      .size() \
      .reset_index(name='count')
   return core_df


# offer slicing and dicing choices for value selection (all value, range, point)
def enhanced_numeric_selection(core_df: pd.DataFrame, col_name: str) -> list:
   """ Offers choices for slicing, dicing. """
   # OOP chains
   options = [f"all {col_name}", f"{col_name} range", f"a specific {col_name}"]
   option_choice = None
   while option_choice == None:
      option_choice = Menu(options).display_with_index().custom_prompt(f"Your filter method for {col_name}: ").validate_with_index()
   all_col_values = Menu(core_df[col_name]).return_as_list()
   var1, var2, var3 = None, None, None
   if option_choice == f"all {col_name}":
      return all_col_values
   elif option_choice == f"{col_name} range":
      while var1 == None:
         var1 = Menu(core_df[col_name]).display_with_values().custom_prompt(f"The start {col_name} of interest: ").validate_with_values()
      while var2 == None:
         var2 = Menu(core_df[col_name]).display_with_values().custom_prompt(f"The end {col_name} of interest: ").validate_with_values()
         small_var = min(int(float(var1)), int(float(var2)))
         large_var = max(int(float(var1)), int(float(var2)))
      return [x for x in all_col_values if small_var <= x <= large_var]
   elif option_choice == f"a specific {col_name}":
      while var3 == None:
         var3 = Menu(core_df[col_name]).display_with_values().custom_prompt(f"For your {col_name} of interest: ").validate_with_values()
      return [int(float(var3))]


# offer slicing and dicing choices for value selection (all value, one to many)
def enhanced_text_selection(core_df: pd.DataFrame, col_name: str) -> list:
   """ Offers choices for slicing, dicing. """
   # OOP chains
   options = [f"all {col_name}", f"one to many {col_name}"]
   option_choice = None
   while option_choice == None:
      option_choice = Menu(options).display_with_index().custom_prompt(f"Your filter method for {col_name}: ").validate_with_index()
   all_col_values = Menu(core_df[col_name]).return_as_list()
   if option_choice == f"all {col_name}":
      return all_col_values
   elif option_choice == f"one to many {col_name}":
      split_str_index = Menu(core_df[col_name]).display_with_index().split_prompt().split_validation_with_index()
      split_int_index = Menu.list_items_as_int(split_str_index)
      split_col_values = [all_col_values[i] for i in split_int_index]
      return split_col_values


# enhanced crash_report with feature 1, 2, 3, 4
# feature 1 & 3, Validate user input
#     catch non-existing report years
#     give meaningful error msg feedback, no record, out of bound
#     provide valid year options in the dataset (unique, non-null year values)
# feature 4, add all possible years options to crash severity report
def crash_severity_report(core_df: pd.DataFrame) -> pd.DataFrame:
   """ Print crash report with specific year and effective speed limit. """
   # Rstudio report <- df %>% mutate %>% select %>% filter %>% group_by %>% summurize
   # offer choices for all possible years, year range, single year
   print("Choose your crash year of interest ↓↓↓")
   year_of_interest = enhanced_numeric_selection(core_df, 'crashYear')
   # offer choices for all possible speed, speed range, single speed
   print("Choose your speed limit of interest ↓↓↓")
   speed_of_interest = enhanced_numeric_selection(core_df, 'effectiveSpeedLimit')
   # offer choices for all possible crash severity type
   print("Choose your crash severity of interest ↓↓↓")
   crash_of_interest = enhanced_text_selection(core_df, 'crashSeverity')
   # reshaping crash_df to generate report
   row_conditions = (core_df['crashYear'].isin(year_of_interest) & 
                     core_df['effectiveSpeedLimit'].isin(speed_of_interest) & 
                     core_df['crashSeverity'].isin(crash_of_interest))
   col_conditions = ['crashYear', 'crashSeverity', 'effectiveSpeedLimit', 'count']
   report = core_df \
      .loc[row_conditions, col_conditions] \
      .groupby(['crashYear', 'crashSeverity']) \
      .agg({'count': 'sum'}) \
      .unstack('crashSeverity') \
      .reset_index()
   return report

# feature 5, generate over time graph based on report result
#     as an extention from crash severity report
def plot_crash_trends(plot_df: pd.DataFrame) -> None:
   """ Plot crash trends using matplotlib.pyplot. """
   # plot each severity as a line
   plot_df = plot_df.set_index('crashYear')
   plot_df.columns = plot_df.columns.get_level_values(-1)
   plot_df.plot(kind='line', marker='o')
   plt.title("Crash Trends by Year")
   plt.xlabel("Crash Year")
   plt.ylabel("Number of Crashes")
   plt.grid(True)
   plt.tight_layout()
   plt.legend(title='Crash Severity')
   plt.show()


# if main
if __name__ == '__main__':
   # load data
   print("testing for enhanced_text_selection")
   raw_df = df_loaded_from_file(DATA_FILE)
   crash_severity_core_df = core_crash_severity_data(raw_df)
   print()

   # enhanced_numeric_selection
   print("testing for enhanced_numeric_selection")   
   selection = enhanced_numeric_selection(crash_severity_core_df, "crashYear")
   print(selection)
   print()

   # enhanced_text_selection
   print("testing for enhanced_text_selection")
   selection = enhanced_text_selection(crash_severity_core_df, 'crashSeverity')
   print(selection)
   print()

   # crash severity report
   print("testing for crash severity report")
   report_for_plot = crash_severity_report(crash_severity_core_df)
   print(report_for_plot)
   print()

   # over time graph
   print("testing for crash over time graph")
   plot_crash_trends(report_for_plot)

