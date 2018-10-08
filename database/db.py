from database import settings as d_settings
from products import settings as p_settings

import json

# Import json and open product.json instead of use 'u_products' from 'products.data.Save' in case of an error / crash.
# Just to avoid downloading again the JSON ...

"""
Class to Drop / Create / Update database, tables and data.
"""


class Database:
    """
    Class to Drop / Create / Update database, tables and data.
    """

    def __init__(self, connection):
        self.connection = connection
        self.products = json.load(open('products.json', 'r'))

    def create(self):
        """
        Drop and create database.
        Drop and create tables according to 'database'.'settings'.'CREATE_TABLE'.
        """

        try:
            with self.connection.cursor() as mysql:
                # DROP & CREATE Database #
                mysql.execute("DROP DATABASE IF EXISTS `pur_beurre`")
                mysql.execute("CREATE DATABASE IF NOT EXISTS `pur_beurre`")
                mysql.execute("USE `pur_beurre`")
                mysql.execute("SET default_storage_engine = InnoDB")
                # DROP Tables #
                for i in range(0, len(d_settings.DROP_TABLES)):
                    drop_tables = "DROP TABLE IF EXISTS " + d_settings.DROP_TABLES[i]
                    mysql.execute(drop_tables)
                # CREATE Tables #
                for i in range(0, len(d_settings.CREATE_TABLE)):
                    mysql.execute(d_settings.CREATE_TABLE[i])
        finally:
            self.connection.commit()

    def update(self):
        """
        Update tables from 'products.json'
        """

        try:
            with self.connection.cursor() as mysql:
                # INSERT Allergens #
                for v in p_settings.ALLERGEN_LIST:
                    insert_allergens = "INSERT IGNORE INTO `pb_allergen` (`allergen_name`) VALUES (%s)"
                    mysql.execute(insert_allergens, v)
                # INSERT Labels #
                for v in p_settings.LABEL_LIST:
                    insert_labels = "INSERT IGNORE INTO `pb_label` (`label_name`) VALUES (%s)"
                    mysql.execute(insert_labels, v)
                # INSERT Stores #
                for v in p_settings.STORE_LIST:
                    insert_stores = "INSERT IGNORE INTO `pb_store` (`store_name`) VALUES (%s)"
                    mysql.execute(insert_stores, v)
                # INSERT Categories #
                for i in range(0, len(self.products)):
                    insert_categories = "INSERT IGNORE INTO `pb_category` (`category_name`) VALUES (%s)"
                    mysql.executemany(insert_categories, (self.products[i]['main_category'],
                                                          self.products[i]['parent_category'],
                                                          self.products[i]['child_category']))
                # INSERT Products #
                for i in range(0, len(self.products)):
                    insert_products = (
                        "INSERT IGNORE INTO `pb_product` VALUES ("
                        "%s, %s, %s,"
                        "(SELECT `id` FROM `pb_category` WHERE %s = `category_name`),"
                        "(SELECT `id` FROM `pb_category` WHERE %s = `category_name`),"
                        "(SELECT `id` FROM `pb_category` WHERE %s = `category_name`),"
                        "%s, %s"
                        ")"
                    )
                    mysql.execute(insert_products, (self.products[i]['id'],
                                                    self.products[i]['name'],
                                                    self.products[i]['description'],
                                                    self.products[i]['main_category'],
                                                    self.products[i]['parent_category'],
                                                    self.products[i]['child_category'],
                                                    self.products[i]['nutrition_score'],
                                                    self.products[i]['link']))
                    # INSERT Products_Allergens #
                    for v in self.products[i]['allergens']:
                        if self.products[i]['allergens'][v] == 1:
                            insert_p_allergens = (
                                "INSERT IGNORE INTO `pb_product_allergen` (`product_id`, `allergen_id`)"
                                "VALUES ("
                                "(SELECT `id` FROM `pb_product` WHERE %s = `pb_product`.`id`),"
                                "(SELECT `id` FROM `pb_allergen` WHERE %s = `pb_allergen`.`allergen_name`))"
                            )
                            mysql.execute(insert_p_allergens, (self.products[i]['id'], v))
                    # INSERT Products_Labels #
                    for v in self.products[i]['labels']:
                        if self.products[i]['labels'][v] == 1:
                            insert_p_labels = (
                                "INSERT IGNORE INTO `pb_product_label` (`product_id`, `label_id`)"
                                "VALUES ("
                                "(SELECT `id` FROM `pb_product` WHERE %s = `pb_product`.`id`),"
                                "(SELECT `id` FROM `pb_label` WHERE %s = `pb_label`.`label_name`))"
                            )
                            mysql.execute(insert_p_labels, (self.products[i]['id'], v))
                    # INSERT Products_Stores #
                    if self.products[i]['stores']:
                        for v in self.products[i]['stores']:
                            insert_p_stores = (
                                "INSERT IGNORE INTO `pb_product_store` (`product_id`, `store_id`)"
                                "VALUES ("
                                "(SELECT `id` FROM `pb_product` WHERE %s = `pb_product`.`id`),"
                                "(SELECT `id` FROM `pb_store` WHERE %s = `pb_store`.`store_name`))"
                            )
                            mysql.execute(insert_p_stores, (self.products[i]['id'], v))
        finally:
            self.connection.commit()
