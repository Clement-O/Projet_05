import json
import random

from products import api, scan
from database import db

"""
Contain Classes to start DataBase creation or use the latter.
"""


class Pb:
    """
    Open External JSON File to get launch state.
    Launch appropriate scripts.
    Switch launch state.
    Update database.
    Display products & substitute.
    """

    def __init__(self, connection, data):
        self.database = db.Database(connection)
        self.data = data
        self.category_list = []
        self.random_products = []
        self.id_chosen_product = 0
        self.substitute = []
        self.digits = [v for k in self.data if k == 'digits' for v in self.data[k]]

    def launch(self):
        """
        Create Database and Tables at first launch.
        """
        self.database.create()

    def update(self):
        """
        Query OpenFoodFacts ('Off'), sort fetched data and save them to update database right after.
        """
        print("+----------------------------------------------------------+\n"
              "|                   Updating Database...                   |\n"
              "+----------------------------------------------------------+\n")
        # Get JSON Products #
        off = api.Off()
        off.page_limit()
        off.raw_data()
        products = scan.Products(off.api_products)
        products.sorted()
        products.unique()
        # Update Database from JSON #
        self.database.update()
        # Print Database updated #
        print("+----------------------------------------------------------+\n"
              "|              The Database has been updated.              |\n"
              "+----------------------------------------------------------+\n")

    def switch(self):
        """
        Switch First launch state (to False).
        """
        self.data['first_launch'] = False
        file = open('settings.json', 'w')
        json.dump(self.data, file, indent=4, separators=(', ', ': '))
        file.close()

    def display_categories(self):
        """
        Display category list
        """
        for value in self.database.query("category"):
            s_list = list(value)
            for idx, letter in enumerate(s_list):
                if letter == '-':
                    s_list[idx] = ' '
            category_name = ''.join(s_list)
            self.category_list.append(category_name.capitalize())
        print("------------------------ CATEGORIES ------------------------")
        print("     Type one of the digits to select a category :")
        for i in range(0, 10):
            print(str(self.digits[i]) + " : " + self.category_list[i])

    def display_products(self, user_input):
        """
        Display product list
        """
        print(
            "------------------------- PRODUCTS -------------------------\n"
            f"You choose \"{self.category_list[self.digits.index(user_input)]}\" category !\n"
            "   Type one of the digits to select a product :"
        )
        self.random_products = random.sample(self.database.query("products", self.digits.index(user_input)), 10)
        for i in range(0, len(self.random_products)):
            print(str(self.digits[i] + " : " + self.random_products[i][1]))

    def display_substitute(self, user_input):
        """
        Display chosen substitute
        """
        self.id_chosen_product = self.random_products[self.digits.index(user_input)][0]
        print(
            "------------------------ SUBSTITUTE ------------------------\n"
            f"You choose \"{self.random_products[self.digits.index(user_input)][1]}\" as product !\n"
        )
        self.substitute = self.database.query("substitute", self.random_products[self.digits.index(user_input)][0])

        if self.substitute:
            stores = ''
            stores_list = []
            for i in range(0, len(self.substitute)):
                stores_list.append(self.substitute[i][5])
            if stores_list:
                stores = ', '.join(stores_list)
            print(
                f"Your product nutrition score is {self.random_products[self.digits.index(user_input)][2]}\n"
                "   It has been replaced by :\n"
                f"       - Name : {self.substitute[0][1]}\n"
                f"       - Description : {self.substitute[0][2]}\n"
                f"       - Nutrition score : {self.substitute[0][3]}\n"
                f"       - Store(s) : {stores}\n"
                f"       - Link : {self.substitute[0][4]}\n\n"
                "You can now save your product and its substitute by typing 'SAVE' "
                f"or search another one with '{self.data['find'][0]}' (or '{self.data['find'][1]}') :"
            )
            return True
        else:
            print(
                "No substitute has been found. Either the product you chose is already the \"best\"\n"
                "or the product does not have \"nutrition score\" (such as Water) or is unknown."
            )
            return False

    def manage_substitute(self, string):
        """
        Display saved substitutes / Manage substitute to be saved (or deleted, not implemented)
        """
        if string == 'save':
            self.database.query('save', self.id_chosen_product, self.substitute[0][0])
            print("Your product and its substitute has been saved ! You can access it via the main menu.\n")
        if string == 'saved':
            r_query = self.database.query('saved')
            num = 1
            print("---------------------- SAVED PRODUCTS ----------------------\n")
            for i in range(0, len(r_query)):
                if not i % 2:
                    print(
                        f"Product & Substitute number {str(num)}\n"
                        f"      Original product >> "
                        f"Name : {r_query[i][0]}, Nutrition score : {r_query[i][1]}\n"
                        f"      Substitute product >> "
                        f"Name : {r_query[i+1][0]}, Nutrition score : {r_query[i+1][1]}, Link : {r_query[i+1][2]}\n"
                    )
                    num += 1
            print(
                f"Type '{self.data['menu'][0]}' (or '{self.data['menu'][1]}') to get back to the menu "
                f"or find a product by typing '{self.data['find'][0]}' (or '{self.data['find'][1]}') :"
                )


class Choice:
    """
    Input class for user's choice.
    """

    def __init__(self, data):
        self.data = data
        self.user_input = ""
        self.word = []
        self.digits = [v for k in self.data if k == 'digits' for v in self.data[k]]
        for k in self.data:
            if k == 'menu' or k == 'saved' or k == 'find' or k == 'update' or k == 'quit':
                for v in self.data[k]:
                    self.word.append(v)

    def menu(self):
        """
        Print "Menu" and wait for input
        """
        self.user_input = input(
            f"\n"
            f"+-------------------------- MENU --------------------------+\n"
            f"  - '{self.data['saved'][0]}' (or '{self.data['saved'][1]}') to display previously saved substitute\n"
            f"  - '{self.data['find'][0]}' (or '{self.data['find'][1]}') to find a substitute\n"
            f"  - '{self.data['update'][0]}' (or '{self.data['update'][1]}') to update database\n"
            f"  - '{self.data['quit'][0]}' (or '{self.data['quit'][1]}') to exit\n"
            f"+----------------------------------------------------------+\n"
            f"Type the word (or letter) in quote marks you want to access :\n"
            f"   => "
        )
        while self.user_input not in self.word:
            self.user_input = input(
                "Invalid value !\n"
                "Please type one of the word or letter in quote marks.\n"
                "   => "
            )

    def categories(self):
        """
        Wait for input and check if input is valid or not.
        """
        self.user_input = input("   => ")
        while self.user_input not in self.digits:
            self.user_input = input(
                "Invalid value ! Please enter a valid digit.\n"
                "   => "
            )

    def products(self):
        """
        Wait for input and check if input is valid or not.
        """
        self.user_input = input("   => ")
        while self.user_input not in self.digits:
            self.user_input = input(
                "Invalid value ! Please enter a valid digit.\n"
                "   => "
            )

    def substitute(self):
        """
        Wait for input and check if input is valid or not.
        """
        self.user_input = input("   => ")
        # Hidden default choice : 'MENU' ('m') or 'QUIT' ('q')
        if self.user_input == 'SAVE':
            return 'save'
        if self.user_input == self.data['menu']:
            return self.data['menu'][0]
        else:
            while self.user_input not in self.word:
                self.user_input = input(
                    "Invalid value ! Please type one of the word or letter in quote marks.\n"
                    "   => "
                )
            return self.user_input
