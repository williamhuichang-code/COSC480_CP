# Part Two Features
- There were two major shifts in my coding style throughout the project, particularly noticeable around week 5 and week 8.
- Week 1 to Week 5:
    - My primary focus was simply to make the code functional. However, I encountered limitations due to my lack of familiarity with libraries like pandas and matplotlib.
- Week 5 to Week 7 (the first major shift):
    - After watching Module 5 and reflecting on my struggles with excessive function complexity, I shifted my focus toward decomposing code for better elegance and readability. I realized that without clear structure, even I would get lost navigating my own functions.
- Week 8 onward (the second major shift):
    - Inspired by the %>% pipeline in RStudio, I began thinking about "Pypelines" (my own term for Python-style pipelines). This sparked a transition to a more object-oriented programming (OOP) approach, where:
        - First, I aimed to design chains of class methods, allowing the output of one method to naturally feed into the next as the first argument.
        - Second, I worked on greatly improving clarity and readability. I modularized my code across multiple files, and structured imports carefully in main.py.
        - Third, I intentionally avoided unnecessary for loops, particularly for large datasets, and focused on leveraging vectorized operations from pandas and matplotlib to minimize time complexity.

## 1. Validate user input: Crash Severity Report
**How I Implemented This Feature**
- My implementation of input validation is based on two key ideas:
    - Standardized Comparison — Both the user input and the option list are first standardized before being compared, ensuring consistent and reliable validation.
    - OOP-Driven Menu Interaction — The validation process follows an object-oriented design: the menu displays itself, prompts the user for input, validates the input against either option indices or values, provides success or error feedback, and ultimately returns a validated user choice.
**The Coding Choices I Made and Why**
- Coding Choices for Option List Standardization:
    - Columns like crashYear or speedLimit often contain many values. To standardize valid options for user input, I created a Menu class. When passed a list, the initializer automatically applies dropna(), unique(), and tolist() in succession.
- Coding Choices for User Input Standardization:
    - I built a CleanInput class (a subclass of str) to flexibly cleanse user inputs. Currently used for fields like crashYear and speedLimit, it processes entries via CleanInput.general_style(), stripping whitespace and formatting inputs into standardized float-type strings. The class is designed to be expandable, allowing additional input-cleaning styles to be easily added in future projects.
- Coding Choices for Validation Process:
    - Once both options and inputs are standardized, the Menu.validate_with_index() method reliably validates user selections by direct comparison.
- Why the Coding Choices:
    - Philosophically, validation should compare standardized inputs against standardized options, not expect perfect inputs. 
    - Code-wise, an OOP approach was natural: encapsulating valid choices in a Menu object aligns with how validation fundamentally operates — by comparison.

## 2. Use Temporary Speed Limit if Defined Instead of Normal Speed Limit
**How I Implemented This Feature**
- To implement this feature, I introduced a new column in the crash dataframe called effectiveSpeedLimit. This column prioritizes the temporarySpeedLimit value if it is available; otherwise, it defaults to the speedLimit value.
- The rest of the report then uses effectiveSpeedLimit instead of speedLimit, so that any logic or filtering automatically respects temporary overrides.
**The Coding Choices I Made and Why**
- Coding Choices and Their Reasoning for Fallback Logic:
    - I created a df_with_effective_speed function to add an effectiveSpeedLimit column, prioritizing temporarySpeedLimit over speedLimit. Encapsulating this in a function ensures clear separation of concerns and improves code readability.
    - This new DataFrame is built inside core_crash_severity_data to provide a centralized, reliable foundation for future reporting and graphing. The implementation follows a "mutate and select" pattern to maintain data integrity.
- Coding Choices and Their Reasoning for combine_first():
    - Initially, I used .apply() with a custom is_numeric() check to capture a broader range of real-world data issues. However, after further analysis, I switched to combine_first() for this crash dataset because:
        - combine_first() naturally supports fallback logic (using the second value when the first is missing).
        - With 856,274 rows, its vectorized operations offer better scalability than row-by-row .apply().
        - Given that temporarySpeedLimit values are mostly clean (mostly valid numbers and occasional NaNs), combine_first() strikes the best balance between robustness and efficiency. Unique values in temporarySpeedLimit are [nan, 30.0, 70.0, 50.0, 40.0, 20.0, 80.0, 60.0, 10.0, 90.0, 45.0, 8.0, 100.0, 75.0, 65.0].
- The initial .apply() code I used before .combine_first():
```python
crash_dataframe["effectiveSpeedLimit"] = crash_dataframe.apply(
    lambda row: row["temporarySpeedLimit"] if is_numeric(row["temporarySpeedLimit"]) else row["speedLimit"],
    axis=1
)
``` 

## 3. Warn the User if No Records Are Found
**How I Implemented This Feature**
- A validation process after the user's selection determines whether any matching records exist. This ensures that even valid inputs, such as requesting a report for 2025, will not silently proceed if there is no actual data associated with them.
**The Coding Choices I Made and Why**
- Essentially, the year 2025 is compared against a list of valid years, with both values standardized as float-type strings. This comparison is handled by my custom function enhanced_numeric_selection, which processes user selections when a specific year is chosen as a report filter. The overall design of enhanced_numeric_selection allows it to universally catch similar mismatches across different columns, including crashYear, speedLimit, and even crashSeverity.
- On the interactive level, every menu-based input prompt includes a display stage before validation, following an object-oriented (OOP) validation chain implemented universally in Feature 1. However, if a user still enters an out-of-range value like 2025, despite seeing available options (e.g., 2000–2024), the error is caught by the validate_with_values method in the Menu class. In this case, an appropriate "no match" message is triggered to inform the user that no matching record exists for the selected year. The system then loops back, redisplaying the valid crashYear options for the user to make a new selection.
- To provide error messages, I centralized all feedback within the rand_msg() function inside the Menu class. This function handles different error and success scenarios, and for each error type, it offers multiple message variations selected randomly using random.choice(), helping avoid repetitive or monotonous prompts.

## 4. Add All Years Option — Crash Severity Report
**How I Implemented This Feature**
- I expanded the crash severity report filtering options by introducing an "All Years" selection. In the enhanced_numeric_selection function, when the user is prompted to choose a crash year, they can now select:
    - All crash years,
    - A year range, or
    - A specific year.
- If "All crash years" is selected, the system includes all available years from the dataset without requiring additional input.
**The Coding Choices I Made and Why**
- The overall structure of the crash_severity_report function follows a pipeline-style design, similar to the RStudio workflow:
    - report <- df %>% mutate() %>% select() %>% filter() %>% group_by() %>% summarize().
- Within this framework, the "All Years" option is implemented as part of the filtering stage, using .loc to apply row_conditions, which are constructed in list format. This design keeps the data transformation process modular and intuitive, allowing flexible user-driven filtering while maintaining the integrity of the reporting pipeline.
- I introduced a menu-driven structure within enhanced_numeric_selection to offer three distinct filtering paths: selecting all values, selecting a range of values, or selecting a single specific value. This structure aligns seamlessly with the broader feature set: supporting the "All Years" option for Feature 4, single-year selections for standard crash severity reports, and providing all-year data as the base for plotting crash trends over time in Feature 5.

## 5. Implement Crash Reports Over Time Graph
**How I Implemented This Feature**
- Initially, I considered building the Over Time Graph as a standalone function with its own separate user input prompts. However, after developing the enhanced_numeric_selection function for flexible year selection in the crash severity report, I realized that these two features could naturally be integrated into a unified workflow.
- enhanced_numeric_selection already allowed users to select across all years, a year range, or a specific year, and could also be easily reused to handle filtering by speed limits. The remaining challenge was enabling flexible user selection of crash severity types (e.g., Minor Crash, Non-Injury Crash).
- To solve this, I developed the enhanced_text_selection function, which mirrors the numeric selection structure but is specifically tailored for textual categories where range-based filtering does not apply. enhanced_text_selection provides users with two main options: selecting all crash types, or selecting one or multiple specific crash types. This unified design allows the report and the time series graph to share the same input selection architecture, ensuring consistency, flexibility, and scalability.
**The Coding Choices I Made and Why**
- Unifying Input Selection Across Features:
    - Rather than writing isolated input prompts for each feature, I built modular selection functions (enhanced_numeric_selection and enhanced_text_selection) that can be reused across different reporting and visualization tasks.
    - This ensures that any future additions or changes (such as adding more filter conditions) can be implemented consistently without redundant code.
- Seamless Slicing and Dicing Design Across Data Types:
    - I approached user input design from a slicing and dicing perspective: empowering users to flexibly partition the dataset according to their specific needs.
    - For numeric fields like crashYear and effectiveSpeedLimit, the enhanced_numeric_selection function enables three slicing options:
        - Selecting all values (no slicing),
        - Selecting a continuous range of values (e.g., years 2010–2015),
        - Selecting a specific single value (e.g., year 2022).
    - For categorical fields like crashSeverity, where range logic does not apply, I developed the enhanced_text_selection function to enable:
        - Selecting all available crash types,
        - Or slicing flexibly across multiple specific crash types (e.g., "Non-Injury Crash" and "Minor Crash" together).
    - By standardizing slicing and dicing across both numeric and text dimensions, the system provides a powerful, consistent user experience that supports a wide range of exploratory analysis needs.