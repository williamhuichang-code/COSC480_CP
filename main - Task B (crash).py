import pandas as pd
import random
import matplotlib.pyplot as plt

DATA_FILE = "data/Crash_Analysis_System_(CAS)_data.csv" ## no raw string notation needed for forward slashes
CONDITION = "fine" ## maybe for future use? data cleaning?

## student feature 1: 
## create a constraint dictionary to hold all the option limits for readability and convenience
constraint_dict = {
    "menu_options": ["Crash Severity Report", 
                     "Crash Reports Over Time Graph", 
                     "Vehicle Types and Crash Severity Graphing",
                     "Cross-Sectional Sampling", 
                     "Sampling Based On Interpretation", 
                     "Exit"], 
    "data_interpretation": {
        "Geospatial Data": [
            "X", "Y", "areaUnitID", "meshblockId", "region", "tlaId", "tlaName"], 
        "Crash Details": [
            "OBJECTID", "crashDirectionDescription", "crashFinancialYear", 
            "crashLocation1", "crashLocation2", "crashRoadSideRoad", 
            "crashSeverity", "crashSHDescription", "crashYear", 
            "directionRoleDescription"], 
        "Environmental and Road Conditions": [
            "advisorySpeed", "flatHill", "holiday", "light", "NumberOfLanes", 
            "roadCharacter", "roadLane", "roadSurface", "roadworks", "slipOrFlood", 
            "speedLimit", "streetLight", "temporarySpeedLimit", "urban", 
            "weatherA", "weatherB"], 
        "Casualty and Severity Information": [
            "fatalCount", "minorInjuryCount", "seriousInjuryCount"],
        "Vehicle and Object Involvement": [
            "bicycle", "bus", "carStationWagon", "fence", "houseOrBuilding", 
            "moped", "motorcycle", "objectThrownOrDropped", "otherObject", 
            "otherVehicleType", "parkedVehicle", "pedestrian", "phoneBoxEtc", 
            "postOrPole", "schoolBus", "suv", "taxi", "train", "tree", "truck", 
            "unknownVehicleType", "vanOrUtility", "vehicle"], 
        "Infrastructure and Obstacles": [
            "bridge", "cliffBank", "ditch", "guardRail", "intersection", 
            "kerb", "trafficControl", "trafficIsland", "trafficSign"], 
        "Potential Hazards": [
            "debris", "overBank", "strayAnimal", "waterRiver"]
        },
    "placeholders": ["just placeholders for now"]
    }

## student feature 2: 
## create a input validation looping function to replace menu_select() with option constraint validation check, importing random
def input_validation_loop(constraint_lst):
    validation = "Not well defined."
    trial_count = 0
    while validation == "Not well defined.":
        print("The valid options are as below:")
        for i in range(len(constraint_lst)):
            print(f"[{i}]: {constraint_lst[i]}")
        user_input = int(input("Please type your choice number: "))
        print()
        if user_input in range(len(constraint_lst)):
            validation = constraint_lst[user_input]
            print(f"you have chosen a valid option {validation}")
            return validation
        else:
            trial_count += 1
            print("Your input is not valid.")
            if trial_count > 5:
                print(f"You've tried {trial_count} times!")
                print("It's really exhausting, and you should really take some rest :D")
                validation = random.sample(constraint_lst, 1)[0]
                print(f"A random choice '{validation}' is assigned instead.")
                return validation
            print("Maybe, you can choose again.\n")

## student feature 4: 
## create a sampling function for data understanding, based on pandas df.loc[] method
def enhanced_sampling(filename, row_entities = None, col_vars = None):
    """
    Read by entities and variables, both vertical and cross-sectional.
    """
    df = pd.read_csv(filename)
    if row_entities == None and col_vars == None:
        # data understanding scenario: perform cross-sectional entity examining
        pd.set_option('display.max_columns', 100)
        sampling = df.loc[random.sample(range(df.shape[0]), 1), df.columns]
    elif row_entities != None and col_vars != None:
        # data understanding scenario: accurate sub-dataframe
        sampling = df.loc[row_entities, col_vars]
    elif row_entities == None and col_vars != None:
        # column-filtered sub-dataframe scenario: you wanna keep all the entities
        sampling = df.loc[list(range(df.shape[0])), col_vars]
    elif row_entities != None and col_vars == None:
        # statistical n>=30 sampling scenario: with data cleaning issue alarming
        print("Warning: Data shall be cleaned before sampling so as to avoid na/duplicates.")
        sampling = df.loc[random.sample(range(df.shape[0]), 30), df.columns]
    return sampling

# original function 1
def read_csv_data(filename: str, columns: list[str]) -> list[tuple]: ## it should be interpreted as reading entities/instances
    """
    IMPORTANT NOTE:
      When completing Part one and Part Two of the project you do NOT need to understand how this function works.
    Reads in data from a list of csv files.
    Returns columns of data requested, in the order given in
    """
    df = pd.read_csv(filename)
    desired_columns = df[columns]
    return list(desired_columns.itertuples(index=False, name=None)) ## suspicious, wait for checking

# original function 2
def menu_select(options: list[str]) -> int: ## i dont really like this loop, while + for is much clearer for readability
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

# original function 3
def unique_values(table: list, col_index: int) -> list: # this is for calculating levels of column variables
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

# original function 4
def print_crash_severity_report(year_of_interest: int, speed_of_interest: int) -> None:
    """Prints a table outlining the number of crashes in a given year for a given speed limit""" ## the output is not a table
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

# original function 5
def main():
    """Small application that presents tables and graphs based on crash data"""
    ## student feature x:
    ## alter main() function to apply new features, and change main() into a while loop with "Exit" option as the way out
    while True:
        main_menu = constraint_dict["menu_options"]
        option = input_validation_loop(main_menu)
        if option == "Crash Severity Report":
            year = int(input("Year: "))
            speed_limit = int(input("Speed Limit: ")) ## typo, should be Speed Limit
            print_crash_severity_report(year, speed_limit)
        elif option == "Crash Reports Over Time Graph":
            print("This part has not been implemented yet, come back later.")
        elif option == "Cross-Sectional Sampling":
            print("Inquiry a random entity with all the columns and columns types for data understanding.\n")
            cross_section_instance = enhanced_sampling(DATA_FILE)
            print(cross_section_instance)
        ## student feature 4: 
        ## build a data udnerstanding option based on variable interpretation groups
        elif option == "Sampling Based On Interpretation":
            groups = list(constraint_dict["data_interpretation"].keys())
            group_name = input_validation_loop(groups)
            group_variable_list = constraint_dict["data_interpretation"][group_name]
            filtered_by_columns = enhanced_sampling(DATA_FILE, col_vars=group_variable_list)
            randomed_instances = random.sample(range(filtered_by_columns.shape[0]), 30)
            filtered_by_rows = enhanced_sampling(DATA_FILE, row_entities=randomed_instances, col_vars=group_variable_list)
            print(filtered_by_rows)
        elif option == "Vehicle Types and Crash Severity Graphing":
            useful_vars = ["carStationWagon", "bicycle", "bus", "motorcycle", "schoolBus", "suv", "taxi", "train", "truck", "crashSeverity", "vanOrUtility"]
            graphing_sample = enhanced_sampling(DATA_FILE, col_vars=useful_vars)
            graphing_sample = graphing_sample.fillna(0)
            severity_distribution = graphing_sample.groupby('crashSeverity').sum()
            severity_distribution = severity_distribution.T
            relative_proportions = severity_distribution.div(severity_distribution.sum(axis=1), axis=0)
            severity_order = ["Fatal Crash", "Serious Crash", "Minor Crash", "Non-Injury Crash"]
            relative_proportions = relative_proportions[severity_order]
            relative_proportions.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
            plt.title('Relative Proportion of Vehicle Types Across Crash Severity Levels')
            plt.xlabel('Vehicle Type')
            plt.ylabel('Proportion of Crashes')
            plt.show()
        elif option == "Exit":
            print("Bye")
            break

main()

