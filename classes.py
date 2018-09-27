import json

from products import api, scan

"""
Contain Class to start DataBase creation or use this last.
"""


class First:
    """
    Open External JSON File to get launch state.
    Launch appropriate scripts.
    Switch launch state.
    """

    def __init__(self):
        self.data = {}

    def check(self):
        """
        Open External JSON File.
        :return: First launch state (True / False). Type: Bool.
        """
        file = open('constant.json', 'r')
        self.data = json.load(file)
        file.close()
        return self.data['first_launch']

    @staticmethod
    def launch():
        """
        Start querying OpenFoodFacts, sort fetched data and save them.
        """
        # Start DataBase creation #
        off = api.Off()
        off.page_limit()
        off.raw_data()
        products = scan.Products(off.api_products)
        products.sorted()
        products.unique()

    def switch(self):
        """
        Switch First launch state (to False).
        """
        self.data['first_launch'] = False
        file = open('constant.json', 'w')
        json.dump(self.data, file, indent=4, separators=(', ', ': '))
        file.close()
