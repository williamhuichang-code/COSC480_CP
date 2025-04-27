"""This module is designed to clean user's input in general.
   Author: William Hui Chang
   Date: Wed Apr  9 00:38:19 2025
"""


class CleanInput(str):
    """ A string subclass for common text preprocessing styles. """
    # instance methods
    def raw_style(self):
        """ Returns the original string in sub class type. """
        return self
    def general_style(self):
        """ Trims and lowercases the string. """
        decent_text = self.strip().lower()
        if self.is_numeric(decent_text):
            return str(float(decent_text))
        else:
            return decent_text
    def name_style(self):
        """ Trims and capitalizes each word in the string. """
        return self.strip().title()
    def split_style(self):
        """ Accepts split input and standardize it. """
        return self.strip().lower().replace(",", " ").replace(";", " ").replace(".", " ").split()
    @staticmethod
    def is_numeric(dirty_data: str) -> bool:
        """Check if a given string can be converted to a numeric value."""
        try:
            int(float(str(dirty_data).strip()))
            return True
        except (ValueError, TypeError):
            return False


if __name__ == "__main__":
    print(CleanInput("  35 ").general_style())
    print(CleanInput("  hapPy NeW YeAR ").general_style())
    print(CleanInput("  james bond  ").name_style())
    split_value = CleanInput(" Apple, Banana;Cherry. Durian").split_style()
    # split_value = CleanInput(" Apple").split_style()
    print(split_value)
    print(type(split_value))