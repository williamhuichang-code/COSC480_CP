"""This module is designed to be tested when imported to my own program.
   Author: William Hui Chang
   Date: Fri Nov 29 08:51:33 2024
"""

if __name__ == "__main__":
    print("\nThis .py file is being excuted directly\ntesting in git")
elif __name__ == "diy_testing_module":
    print("\nThis .py file is imported/borrowed as a module\ndoes it really work in git as well?\n")
    import this



"""
    # commandlines to test existed module location
        import numpy
        numpy.__file__
    # put my newly created modules in this location
        blabla
"""