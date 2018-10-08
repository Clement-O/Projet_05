import json
import pymysql

import classes

"""
Main python file
"""

# TODO Update Readme.md


def pur_beurre():
    """
    Check if it's the first time launching the script.
        If True     : Call needed algorithm to create database
        If False    : Execute script # TODO Complete description
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

    pb = classes.Pb(connection)

    if data['first_launch']:
        print('First Launch : TRUE')    # TEST Print
        pb.launch()
        pb.update()
        pb.switch(data)
    else:
        print('First Launch : FALSE')   # TEST Print


if __name__ == "__main__":
    pur_beurre()
