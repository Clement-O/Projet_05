import json
import pymysql
# Import to ignore warnings of MySQL (such as duplicate).
import sys
import warnings

import classes


"""
Main python file
"""


def pur_beurre():
    """
    Check if it's the first time launching the script.
        If True     : Call needed algorithm to create & update database
        If False    : Interact with user
    """

    # Open "constant" (/ external) settings #
    file = open('settings.json', 'r')
    data = json.load(file)
    file.close()

    # Init mysql connection #
    connection = pymysql.connect(host=data['host'],
                                 user=data['user'],
                                 password=data['password'],
                                 charset='utf8')

    pb = classes.Pb(connection, data)
    choice = classes.Choice(data)

    while choice.user_input not in data['quit']:
        if data['first_launch']:
            pb.launch()
            pb.update()
            pb.switch()
        elif choice.user_input in data['update']:
            pb.update()
            choice.menu()
        elif choice.user_input in data['find']:
            pb.display_categories()
            choice.categories()
            if choice.user_input in data['digits']:
                pb.display_products(choice.user_input)
                choice.products()
                if pb.display_substitute(choice.user_input):
                    if choice.substitute() == 'save':
                        pb.manage_substitute('save')
        elif choice.user_input in data['saved']:
            pb.manage_substitute('saved')
            choice.substitute()
        else:
            choice.menu()


if __name__ == "__main__":
    # Ignore warnings.
    if not sys.warnoptions:
        warnings.simplefilter("ignore")
    pur_beurre()
