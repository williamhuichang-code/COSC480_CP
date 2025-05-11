"""This program is designed to cleanse data, organize, identify trends and
visualize data for ill-specified, complex data-science problems.
   Author: William Hui Chang
   Date: Fri Mar 21 21:06:21 2025
"""

import pandas as pd
from crash_specific_module import core_crash_severity_data, crash_severity_report, plot_crash_trends
from menu_module import Menu
from config_module import DATA_FILE



def df_loaded_from_file(filename: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    print("Now loading ...\n...")
    ready_df = pd.read_csv(filename)
    print("Dataframe has been successfully loaded!")
    return ready_df


def end_of_application() -> bool:
    """Ends the application."""
    print(Menu.rand_msg("bye msg"))
    return True


def general_validation_loop(validation_func: callable) -> str:
    """ Loops a validation function and returns a valid choice. """
    valid_selection = None
    while valid_selection == None:
        valid_selection = validation_func()
    return valid_selection


def main_menu_validation_trial() -> str:
    """ Returns a potential menu selection for looping after a chained function process. """
    main_menu = ["Exit", "Crash Severity Report", "Crash Reports Over Time Graph"]
    return Menu(main_menu).display_with_index().general_prompt().validate_with_index()


def main():
    """ Generates reports and graphs based on crash data. """
    # load df
    raw_df = df_loaded_from_file(DATA_FILE)
    crash_severity_core_df = core_crash_severity_data(raw_df)
    # main menu loop
    terminate = None
    while terminate != True:
        # menu selection validation
        menu_selection = general_validation_loop(main_menu_validation_trial)
        # match choice scenarios
        match menu_selection:
            case "Exit":
                terminate = end_of_application()
            case "Crash Severity Report":
                crash_report = crash_severity_report(crash_severity_core_df)
                print(crash_report)
            case "Crash Reports Over Time Graph":
                report_as_plot = crash_severity_report(crash_severity_core_df)
                plot_crash_trends(report_as_plot)



main()
