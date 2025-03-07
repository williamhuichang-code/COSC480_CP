# Crash Data Analysis

**Author:** William Hui Chang  
**Student ID:** 69051925  
**Date:** March 8, 2025

## 1. Initial Program Behavior:
- Explanation of initial data form.
  The initial dataset is sourced as a csv file by using `pd.read_csv()` function. It includes 856274 observations and 72 variables, as indicated by `df.shape` output. The data seems to document car incidents within a geographical context, with detailed aspects (`df.columns`) related to coordinates (X, Y), crash details (crashSeverity), traffic condition (speedLimit), time series (crashYear), weather situation, vehicle types and potentially other contributing factors.

- Program behaviour regarding user inputs and outputs.
  This program consists of three main steps:
    Step 1: Run the procedure function main() to activate the program and manage the conditional steps. The `main()` function is executed to initialize the program and handle conditional logics.
    Step 2: Display a menu with options for generating a report, a placeholder for a graph, and an option to exit. If user selects option 0 from the displayed choices [0, 1, 2], this input will be validated by the `menu_select()` function, outputting the verified selection of option 1.
    Step 3: When the report option is selected, the program prompts the user to enter a specific year and speed limit. The report then displays the count of crashes by severity type for the selected year and speed limit. More detailed, the main() function uses the selected option as a condition to trigger the `read_csv_data()` and `print_crash_severity_report()` functions. The `unique_values()` function is utilized as a helper tool to generate the unique types of crashSeverity for looping through the severity counts. At this stage, the main() function specifically prompts the user to enter the desired crashYear and speedLimit. The print_crash_severity_report() function then applies these inputs as filter conditions to calculate the count of each crashSeverity type. 
    For example, if the user inputs the year 2000 and speed limit 30, the print_crash_severity_report() function generates a severity count report:
      Fatal Crash: 3
      Minor Crash: 28
      Non-Injury Crash: 231
      Serious Crash: 6

## 2. Dependencies:
- Data (Waka Kotahi) CC BY 4.0
- [Pandas](https://pandas.pydata.org/)
- [Random](https://docs.python.org/3/library/random.html)
- [Matplotlib](https://matplotlib.org/)

## 3. How to Run:
To execute this program run following command from a terminal:

`python3 main - Task B (crash).py`

## 4. Future Development:
###   a) Basic Analysis Feature:
  - Idea 1: Analyzing the Relationship Between Vehicle Types and Crash Severity
    - Objective: Assess whether specific vehicle types correlate with varying degrees of crash severity.
    - Approach: 
      - Identifying relevant variables required for analysis;
      - Perform necessary data preprocessing, like handling NA values and eliminating duplicates;
      - Analyze the distribution of vehicle types in relation to different crash severity levels.
      - Visualize the data using a stakced bar chart:
        - X-axis: Vehicle types as potential explanatory variables.
        - Visualzation Tool: Utilize matplotlib to generate the bar chart.
  - Idea 2: Temporal and Geographical Analysis of Crashes
    - Objective: Investigate potential trends over time and geographical patterns to identify if specific time periods or regions are more prone to crashes.
    - Approach: 
      - Evaluate temporal trends by aggregating crash data;
      Identify potential seasonal factors contributing to observed trends.
      - Utilize line plot to display trends over time and bar charts to visualize crash counts by year using matplotlib.
    - Idea 3: Day vs. Night Analysis of Crash Factors
      - Objective: Examine the influence of daytime and nighttime conditions on crash occurrences to identify potential contributing factors.
      - Approach: 
        - Determine relevant factors influencing crashes during day and night, such as:
          - Daytime: Weather conditions (weatherA, weatherB), holidays, and traffic congestion.
          - Nighttime: Impact of street lighting, visibility, and incidents of drunk driving.
        - Visualize the associations using a heatmap:
          - X-axis: Weather conditions. 
          - Y-axis Lighting conditions.

###   b) Student Lead Features:
  - Completed Features:
    1. Constraint Dictionary: Created a dictionary to store all option limits, enhancing readability and convenience.
    2. Input Validation Function: Developed a robust input validation loop to replace menu_select(), incorporating option constraint checks and utilizing the random module.
    3. Data Sampling Function: Implemented a data sampling method for data exploration using the pandas df.loc[] method, partially integrated into the main() function.
    4. Data Understanding by Variable Groups: Built a feature to facilitate data understanding based on predefined variable interpretation groups.
    5. Main Function Enhancement:
      - Transformed the main() function into a while loop with an "Exit" option as the termination condition.
      - Integrated the new features seamlessly into the main workflow.
    6. Typographical Fix: Corrected a typo in the main() function, changing "Seed Limit" to "Speed Limit" for accurate input prompts.
  - Ongoing Development:
    - Data Cleaning Function: Develop a comprehensive function to handle data cleaning tasks such as:
      - Handling missing values (NA values).
      - Removing duplicates.
      - Standardizing data types and formats.
    - Sampling Strategy Validation:
      - Explore an idea to demonstrate that sample values tend to "hug" the mean.
      - Highlight the significance of Bessel's correction in sample variance (H1 hypothesis).
      - Note: This might extend beyond the core project scope but offers valuable insights.
    - Output Flow Optimization:
      - Introduce time.sleep() from the time module to generate output with a smooth, natural flow.
    - Data Exploration Enhancement:
      - Create a function to dynamically display:
        - Cardinality and value ranges for specific columns.  - Data types (both primitive and statistical).
        - NA values and duplicates.
    - Object-Oriented Refactoring:
      - Transition the project into a class-based, object-oriented approach.
      - Aim for an elegant, modular, and expandable codebase.

## Citations
- Waka Kotahi. _Crash Analysis System (CAS) data_ [Review of  Crash Analysis System (CAS) data]. Retrieved January 13, 2025, from https://opendata-nzta.opendata.arcgis.com/datasets/8d684f1841fa4dbea6afaefc8a1ba0fc_0/explore
