import pandas as pd

DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv"
CONDITION = "fine"


def read_csv_data(filename: str, columns: list[str]) -> list[tuple]:
    """
    IMPORTANT NOTE:
      When completing Part one and Part Two of the project you do NOT need to understand how this function works.
    Reads in data from a list of csv files.
    Returns columns of data requested, in the order given in
    """
    df = pd.read_csv(filename)
    desired_columns = df[columns]
    return list(desired_columns.itertuples(index=False, name=None))


def menu_select(options: list[str]) -> int:
    """
    - Prints a list of enumerated options and collects the users
    - The user is prompted until they enter a valid menu index
    - returns valid user selection
    """
    prompt = f"0-{len(options) - 1}:: "
    i = 0
    while i < len(options):
        print(f'[{i}] {options[i]}')
        i += 1

    selection = int(input(prompt))
    while selection < 0 or selection >= len(options):
        print(f'{selection} is not a valid option\nTry again')
        selection = int(input(prompt))
    return selection


def unique_values(table: list, col_index: int) -> list:
    """Given a list of tuple returns a sorted list of unique values of a given row.
    Example:
    animals = [
        ("cat", "dog"),
        ("bird", "dog"),
        ("fish", "fish")
    ]

    print(unique_values(animals, 0))
    ['bird', 'cat', 'fish']

    print(unique_values(animals, 1))
    ['dog', 'fish']
    """
    out = []
    for row in table:
        if row[col_index] not in out:
            out.append(row[col_index])
    out.sort()
    return out


def print_crash_severity_report(year_of_interest: int, speed_of_interest: int) -> None:
    """Prints a table outlining the number of crashes in a given year for a given speed limit"""
    data = read_csv_data(
        DATA_FILE, ["crashYear", "speedLimit", "crashSeverity"])
    severity_types = unique_values(data, 2)
    print("Crash Severity by Classification")
    print(f"Speed: {speed_of_interest}")
    print(f"Year: {year_of_interest}")
    print()
    for severity_type in severity_types:
        count = 0
        for year, speed_limit, crash_type in data:
            if year == year_of_interest and speed_limit == speed_of_interest and crash_type == severity_type:
                count += 1
        print(f"{severity_type}: {count}")


def main():
    """Small application that presents tables and graphs based on crash data"""
    menu_options = [
        "Crash Severity Report",
        "Crash Reports Over Time Graph",
        "Exit"
    ]
    option = menu_select(menu_options)
    if option == 0:
        year = int(input("Year: "))
        speed_limit = int(input("Seed Limit: "))

        print_crash_severity_report(year, speed_limit)
    elif option == 1:
        print("Not Implemented Yet")
    elif option == 2:
        print("Bye")


main()
