# Part Two Features
Below are a list of features that are to be completed for the second part of the assignment. Refer to the Project section of the course page for more detail on each feature.

Please fill in the section for each feature, replace all text below each heading.

## 1. Validate user input: Crash Severity Report
**How I Implemented This Feature**
- I added a validation system to ensure the user selects a valid crashYear and effectiveSpeedLimit. I used the validated_crash_selection() function to repeatedly prompt the user until they enter a valid input. This function uses a helper, is_crash_input_valid(), which checks whether the user input is numeric and falls within the allowed values. It also cleans the input using cleaned_numeric_input() to handle spaces, floats like " 3.0", and other edge cases.
**The Coding Choices I Made and Why**
- Custom numeric check: Instead of using .isnumeric(), I created an is_numeric() function to handle floating-point values, catch NaN, and avoid crashes from unexpected strings.
- Constraint-based validation: I compared the cleaned user input against a list of valid choices (crashYear and effectiveSpeedLimit) to prevent out-of-range or invalid selections.
- User-friendly retry loop: If input is invalid, the user sees an error message and is prompted again, improving usability and reducing runtime errors.
- Whitespace + case handling: All inputs are cleaned using cleaned_text_input() to tolerate common formatting mistakes, making the system more robust.
**my thoughts for universal validation problems**
- The course material suggests using the .isnumeric() method to validate if user input is numeric. However, I find this approach insufficient, as it does not handle all potential edge cases effectively. Since user input must be converted into a numeric form, several issues arise:
(1) Floating Point Handling:
- The .isnumeric() method does not recognize floating-point numbers. For instance, "3.0".isnumeric() returns False, even though "3.0" should be considered as a valid numeric input.
- Converting "3.0" directly to an integer using int("3.0") results in a ValueError, making it an impractical approach.
- The float() function can correctly handle "3.0", but introduces additional concerns regarding floating-point precision and unexpected behavior in further computations.
(2) NaN (Not a Number) Issue:
- Numeric validation should be designed for broad applicability, ensuring robustness for both user input validation and data cleaning tasks.
- Python treats "nan" as a floating-point value, meaning float("nan") successfully converts it into a nan rather than triggering an error.
- This could lead to hidden errors that are difficult to debug, especially if nan values slip through unnoticed in data validation processes.
- Proper error handling should be implemented to catch such cases explicitly, even though we assume the data has already been cleaned.
(3) Whitespace Handling:
- Users might accidentally include leading or trailing spaces in their input, such as " 7 " instead of "7".
- The .isnumeric() method does not account for this, and both int(" 7 ") and float(" 7 ") will raise a ValueError.
- A robust input validation system should accommodate minor formatting inconsistencies without causing failures.
(4) Input Range Constraints:
- Even if a user provides a valid numeric input, it might fall outside an acceptable range.
- For instance, if only certain menu index numbers are permitted, an input like "12" may pass .isnumeric() but still be invalid for the intended context.
(5) Text String Handling:
- If a user mistakenly enters non-numeric text (e.g., "this should be numeric"), .isnumeric() will return False, which is expected.
- However, attempting to process this invalid input with int() or float() will result in a ValueError, necessitating additional error handling to provide clearer feedback.

**my general solution for universal validations**
a> for open-ended numeric validation
- The key to open-ended validation lies in distinguishing intended numeric inputs that may contain minor formatting issues. 
- Consider two edge cases: " 7.0 " and "nan ". Both include whitespace, but one represents a valid floating-point number, while the other is not a true numeric value. After applying .strip(), using float("7.0") allows "7.0" to pass, which is preferable to int() alone. However, float("nan") also passes — that's where int(float(x)) comes in. Attempting int(float("nan")) raises an error, effectively catching invalid entries like "nan" as desired.
- Therefore, I will use int(float(numeric_string.strip())) as the validation mechanism, and rely on try-except blocks to handle any errors that may arise during conversion, as demonstrated in my function is_numeric(dirty_string).
b> for closed-ended validation, like Menu Option
- For a closed-ended validation like this, the option index is displayed in the menu. Typically, when receiving user input as a string, we might attempt to convert it using int(). However, this approach has a flaw—if the user enters something like "3.0" or non-numeric text, the program will break and raise a ValueError.
- To avoid this, I would consider storing numeric menu indices as strings in a list. This way, when the user inputs a string, we can simply compare it against a list of valid string indices. This approach is more reliable and helps prevent errors, effectively handling cases such as floating-point input or non-numeric text. As demonstrated in my code, validated_index_choice(listed_options), this method ensures smoother validation.
- I think by using my helper function is_numeric(dirty_string) can solve this problem as well, but I think it could be better to try something different.
c> for closed-ended universal validation
- While working on find_column_matches(original_dataframe), I encountered string-matching issues. I realized that for string validation, it's essential to standardize values — for example, using .lower() on user input to ensure consistency.
- At its core, the universal approach to comparison problems like this is to standardize both sides before comparing.
- Validation becomes reliable when you're comparing two standardized forms: one from the user input, and the other from the predefined option list.
- For now, here’s the standard I’m applying:
    - For numeric strings: remove any surrounding whitespace.
    - For numeric values: convert to float; anything unrecognized or invalid will be treated as float('nan').
        - float('nan') acts as an "unknown" placeholder, which is ideal for comparison — because in Python, float('nan') != float('nan'), making it easy to detect mismatches.
- This part c hasn't been implemented yet, but I think it's a very good approach once I have time.


## 2. Use temporary speed limit if defined instead of normal speed limit
**How I Implemented This Feature**
- To implement this feature, I introduced a new column in the crash_dataframe called effectiveSpeedLimit. This column selects the temporarySpeedLimit value if it is defined (i.e., numeric); otherwise, it defaults to the speedLimit value.
- I achieved this using the apply() function with a lambda expression that checks each row. The logic is:

crash_dataframe["effectiveSpeedLimit"] = crash_dataframe.apply(
    lambda row: row["temporarySpeedLimit"] if is_numeric(row["temporarySpeedLimit"]) else row["speedLimit"],
    axis=1
)

- The rest of the report then uses effectiveSpeedLimit instead of speedLimit, so that any logic or filtering automatically respects temporary overrides.

**The Coding Choices I Made and Why**
- Use of apply() with lambda:
    - I chose to use apply() with a row-wise lambda to easily access and compare temporarySpeedLimit and speedLimit within each row. This avoids the need for more verbose for loops or multiple passes through the DataFrame.
- Check for numeric with is_numeric():
    - Since temporarySpeedLimit may be missing or invalid, I used an is_numeric() check to ensure only valid temporary speed limits are used. This guards against errors if the column contains nulls or strings.
- New column effectiveSpeedLimit:
    - Creating a new column instead of overwriting the original speedLimit maintains data integrity and keeps the logic clear. It also helps with debugging and any future changes, as the original values are preserved.
- Seamless integration with existing logic:
    - By simply replacing usage of speedLimit with effectiveSpeedLimit in downstream code, the change was minimally invasive and required no major reworking of existing functions like print_crash_severity_report().

## 3. Warn the user if no records are found  
Replace me with an outline of:

- how you implemented this feature
- choices you made and why


## 4. Add all years: Crash Severity Report
Replace me with an outline of:

- how you implemented this feature
- choices you made and why


## 5. Implement Crash Reports Over Time Graph
Replace me with an outline of:

- how you implemented this feature
- choices you made and why
