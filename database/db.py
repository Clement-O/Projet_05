from database import settings as d_settings
from products import settings as p_settings

import json

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
        self.categories_id = []

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
                mysql.execute("USE `pur_beurre`")
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

    def query(self, string, *arg):
        """
        Query the database to get categories / products / substitutes.
        :param string: To know what to query.
        :param arg: Either user input (Type: String.) or `id` (Type: Int.).
        :return: Query result.
        """
        try:
            with self.connection.cursor() as mysql:
                mysql.execute("USE `pur_beurre`")
                # Categories #
                if string == "category":
                    r_query = []
                    get_categories = (
                        "SELECT `main_category_id`, COUNT(*) FROM `pb_product` "
                        "GROUP BY `main_category_id` "
                        "ORDER BY COUNT(*) DESC "
                        "LIMIT 10"
                    )
                    mysql.execute(get_categories)
                    self.categories_id = mysql.fetchall()
                    get_names = "SELECT `category_name` FROM `pb_category` WHERE `id` = %s"
                    for i in range(0, 10):
                        mysql.execute(get_names, self.categories_id[i][0])
                        fetch_query = mysql.fetchone()
                        r_query.append(fetch_query[0][3:])
                    return r_query  # Type: List.
                # Products #
                elif string == "products":
                    get_products = (
                        "SELECT `id`, `name`, `nutrition_score` FROM `pb_product`"
                        "WHERE `main_category_id` = %s"
                    )
                    mysql.execute(get_products, self.categories_id[int(*arg)][0])
                    r_query = mysql.fetchall()
                    return r_query  # Type: Tuple.
                # Substitute #
                elif string == "substitute":
                    r_query = None
                    get_product = (
                        "SELECT `main_category_id`, `parent_category_id`, `child_category_id`, `nutrition_score` "
                        "FROM `pb_product`"
                        "WHERE `id` = %s"
                    )
                    mysql.execute(get_product, int(*arg))
                    nutrition_score = mysql.fetchone()

                    get_substitute = (
                        "SELECT "
                        "`pb_product`.`id`, "
                        "`pb_product`.`name`, "
                        "`pb_product`.`description`, "
                        "`pb_product`.`nutrition_score`, "
                        "`pb_product`.`link`, "
                        "`pb_store`.`store_name` "
                        "FROM `pb_product`"
                        "INNER JOIN `pb_product_store` "
                        "   ON `pb_product`.`id` = `pb_product_store`.`product_id`"
                        "INNER JOIN `pb_store` "
                        "   ON `pb_product_store`.`store_id` = `pb_store`.`id`"
                        "WHERE pb_product.id = ("
                        "   SELECT pb_product.id "
                        "   FROM pb_product "
                        "   WHERE `main_category_id` = %s "
                        "       AND `parent_category_id` = %s "
                        "       AND `child_category_id` = %s "
                        "       AND `nutrition_score` = %s "
                        "   ORDER BY `nutrition_score` ASC "
                        "   LIMIT 1)"
                    )

                    if (nutrition_score[3] is None) or (nutrition_score[3] == 'A'):
                        return

                    score_list = ['A', 'B', 'C', 'D', 'E']
                    for i in score_list[:score_list.index(nutrition_score[3])]:
                        mysql.execute(get_substitute, (nutrition_score[0], nutrition_score[1], nutrition_score[2], i))
                        r_query = mysql.fetchall()
                        if r_query:
                            return r_query  # Type: Tuple.
                    if r_query is None:
                        return r_query  # Type: None

                elif string == "save":
                    save_substitute = (
                        "INSERT IGNORE INTO `pb_product_substitute` (`original_id`, `substitute_id`) "
                        "VALUES (%s, %s)"
                    )
                    mysql.execute(save_substitute, (arg[0], arg[1]))
                elif string == 'saved':
                    f_query = True
                    r_query = []
                    offset = 0
                    saved_substitute = (
                        "SELECT `name`, `nutrition_score`, `link` "
                        "FROM `pb_product`"
                        "WHERE "
                        "(SELECT `original_id` FROM `pb_product_substitute` LIMIT 1 OFFSET %s) = `id`"
                        "OR "
                        "(SELECT `substitute_id` FROM `pb_product_substitute` LIMIT 1 OFFSET %s) = `id`"
                        "ORDER BY `nutrition_score` DESC"
                    )
                    while f_query:
                        mysql.execute(saved_substitute, (offset, offset))
                        f_query = mysql.fetchall()
                        if f_query:
                            r_query.extend(f_query)
                        offset += 1
                    return r_query
        finally:
            self.connection.commit()
