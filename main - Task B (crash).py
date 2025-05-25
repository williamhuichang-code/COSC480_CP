"""This program is designed to cleanse data, organize, identify trends and
visualize data for ill-specified, complex data-science problems.
   Author: William Hui Chang
   Date: Fri Mar 21 21:06:21 2025
"""

from module_crashdf_features import core_crash_severity_data, crash_severity_report, plot_crash_trends
from class_helper_menu import Menu
from subclass_crashdf import CrashDf



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
    raw_df = CrashDf.df_loaded_with_online_update(CrashDf._crash_csv_name).cleaned_crashdf_by_nz_bounds()
    # raw_df = df_loaded_from_url(crash_url)
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
                report_for_plot = crash_severity_report(crash_severity_core_df)
                plot_crash_trends(report_for_plot)



main()
