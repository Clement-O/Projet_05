import json

from products import api, scan
from database import db

"""
Contain Class to start DataBase creation or use this last.
"""


class Pb:
    """
    Open External JSON File to get launch state.
    Launch appropriate scripts.
    Switch launch state.
    """

    def __init__(self, connection):
        self.connection = connection

    def launch(self):
        """
        Create Database and Tables at first launch.
        """
        database = db.Database(self.connection)
        database.create()

    def update(self):
        """
        Query OpenFoodFacts ('Off'), sort fetched data and save them to update database right after.
        """
        # Get JSON Products #
        off = api.Off()
        off.page_limit()
        off.raw_data()
        products = scan.Products(off.api_products)
        products.sorted()
        products.unique()
        # Update Database from JSON #
        database = db.Database(self.connection)
        database.update()

    @staticmethod
    def switch(data):
        """
        Switch First launch state (to False).
        :param data: Data from 'settings.json' opened in 'pur_beurre.py'.'pur_beurre()'.
        """
        data['first_launch'] = False
        file = open('settings.json', 'w')
        json.dump(data, file, indent=4, separators=(', ', ': '))
        file.close()
