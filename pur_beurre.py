import classes

"""
Main python file
"""


def pur_beurre():
    """
    Check if it's the first time launching the script.
        If True     : Call needed algorithm to create database
        If False    : Execute script # TODO Complete description
    """
    first = classes.First()
    if first.check():
        print('First Launch : TRUE')      # TEST Print
        first.launch()
        first.switch()
    else:
        print('First Launch : FALSE')    # TEST Print


if __name__ == "__main__":
    pur_beurre()
