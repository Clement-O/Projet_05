import json

from products import sort

"""
Create product according to a model. Save sorted products to clear out unique products and save them into JSON file.
"""


class Save:
    """
    Create product according to a model.
    Save sorted products to clear out unique products and save them into JSON file.
    """

    def __init__(self, api_products):
        self.api_products = api_products
        self.s_products = []  # sorted_products
        self.u_products = []  # unique_products
        self.dic = sort.Dictionary(api_products)
        self.excl = sort.Exclusive(self.s_products)

    def sorted_product(self, page_n, product_n, categories, length):
        """
        Create product according to a model.
        Save sorted products to clear out unique products.
        :param page_n: page_number (1 to 'PAGE_LIMIT').
        :param product_n: product_number (1 to 'PAGE_SIZE').
        :param categories: english categories (at least 3, from 'sort.Dictionary.complete()').
        :param length: categories length (from 'sort.Dictionary.complete()').
        :return: 's_products'. Type: List.
        """

        _id = self.api_products[page_n]['products'][product_n]['_id']
        name = self.api_products[page_n]['products'][product_n]['product_name_fr'].capitalize()
        description = self.api_products[page_n]['products'][product_n]['generic_name_fr'].capitalize()
        main_category = categories[0].lower()
        parent_category = categories[length - 1].lower()
        child_category = categories[length].lower()
        stores = self.dic.stores(page_n, product_n)
        allergens = self.dic.allergens(page_n, product_n)
        labels = self.dic.labels(page_n, product_n)
        nutrition_score = self.dic.nutrition_score(page_n, product_n)
        link = "https://fr.openfoodfacts.org/produit/" + _id

        product = {
            'id': int(_id),
            'name': name,
            'description': description,
            'main_category': main_category,
            'parent_category': parent_category,
            'child_category': child_category,
            'stores': stores,
            'allergens': allergens,
            'labels': labels,
            'nutrition_score': nutrition_score,
            'link': link
        }

        self.s_products.append(product)

    def unique_products(self, key):
        """
        Create product according to a model.
        Save unique products.
        :param key: Key of current product being filtered.
        :return: 'u_products'. Type: List.
        """

        _id = self.excl.recursive(key, 'id')
        name = self.excl.recursive(key, 'name')
        description = self.excl.recursive(key, 'description')
        main_category = self.excl.recursive(key, 'main_category')
        parent_category = self.excl.recursive(key, 'parent_category')
        child_category = self.excl.recursive(key, 'child_category')
        stores = self.excl.recursive(key, 'stores')
        allergens = self.excl.recursive(key, 'allergens')
        labels = self.excl.recursive(key, 'labels')
        nutrition_score = self.excl.recursive(key, 'nutrition_score')
        link = "https://fr.openfoodfacts.org/produit/" + str(_id)

        product = {
            'id': _id,
            'name': name,
            'description': description,
            'main_category': main_category,
            'parent_category': parent_category,
            'child_category': child_category,
            'stores': stores,
            'allergens': allergens,
            'labels': labels,
            'nutrition_score': nutrition_score,
            'link': link
        }

        self.u_products.append(product)

    def write(self, del_list):
        """
        Delete duplicated products and save 'u_products' into a JSON File.
        :param del_list: Index of all duplicated products to delete.
        :return: 'u_products'. Type: List & JSON.
        """
        del_list.sort()
        del_list.reverse()
        for i in range(0, len(del_list)):
            del self.s_products[del_list[i]]
        self.u_products.append(self.s_products)

        with open('products.json', 'w', encoding='utf-8') as outfile:
            json.dump(self.u_products, outfile, indent=4, separators=(', ', ': '))
