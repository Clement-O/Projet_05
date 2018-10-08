from products import settings

"""
Contain Class to filter and sort relevant products informations
"""


class Dictionary:
    """
    Filter and sort relevant products informations.
    First Filter. Keep duplicated products.
    """

    def __init__(self, api_products):
        self.api_products = api_products
        self.categories = []
        self.length = -1

    def complete(self, page_n, product_n):
        """
        Check if the product have a french name and description (generic name).
        Also check if it has more than 3 english categories.
        :param page_n: page_number (1 to 'PAGE_LIMIT').
        :param product_n: product_number (1 to 'PAGE_SIZE').
        :return: Product "state". Is it complete (True) or not (False). Type: Bool.
        """
        if self.api_products[page_n]['products'][product_n]['product_name_fr']:
            if self.api_products[page_n]['products'][product_n]['generic_name_fr']:
                for category in self.api_products[page_n]['products'][product_n]['categories_hierarchy']:
                    if category[:2] == 'en':
                        self.categories.append(category)
                        self.length += 1
                if self.length >= 2:
                    return True
        return False

    def stores(self, page_n, product_n):
        """
        Get store(s) for given product, keep those matching 'STORE_LIST' and format it into a List.
        :param page_n: page_n: page_number (1 to 'PAGE_LIMIT').
        :param product_n: product_n: product_number (1 to 'PAGE_SIZE').
        :return: 'stores'. Type: List.
        """
        store_list = []
        if self.api_products[page_n]['products'][product_n]['stores']:
            store_raw = self.api_products[page_n]['products'][product_n]['stores']
            store_split = store_raw.split(',')
            for store in store_split:
                store_strip = store.strip()
                store_list.append(store_strip.title())
            store_set = list(set(store_list).intersection(settings.STORE_LIST))
            if store_set:
                stores = store_set
            else:
                stores = None
        else:
            stores = None
        return stores

    def allergens(self, page_n, product_n):
        """
        Get allergen(s) for given product and format it into a Dict.
        :param page_n: page_n: page_number (1 to 'PAGE_LIMIT').
        :param product_n: product_n: product_number (1 to 'PAGE_SIZE').
        :return: 'allergens'. Type: Dict.
        """
        allergens = {}
        if self.api_products[page_n]['products'][product_n]['allergens_hierarchy']:
            for i in settings.ALLERGEN_LIST:
                allergens.update({i: 0})
                for allergen in self.api_products[page_n]['products'][product_n]['allergens_hierarchy']:
                    if allergen == 'en:'+i:
                        allergens[i] = 1
        else:
            for i in settings.ALLERGEN_LIST:
                allergens.update({i: 0})
        return allergens

    def labels(self, page_n, product_n):
        """
        Get label(s) for given product and format it into a Dict.
        :param page_n: page_n: page_number (1 to 'PAGE_LIMIT').
        :param product_n: product_n: product_number (1 to 'PAGE_SIZE').
        :return: 'labels'. Type: Dict.
        """
        labels = {}
        if self.api_products[page_n]['products'][product_n]['labels_hierarchy']:
            for i in settings.LABEL_LIST:
                labels.update({i: 0})
                for label in self.api_products[page_n]['products'][product_n]['labels_hierarchy']:
                    if label == 'en:'+i:
                        labels[i] = 1
        else:
            for i in settings.LABEL_LIST:
                labels.update({i: 0})
        return labels

    def nutrition_score(self, page_n, product_n):
        """
        Get nutrition_score for given product and format it.
        :param page_n: page_n: page_number (1 to 'PAGE_LIMIT').
        :param product_n: product_n: product_number (1 to 'PAGE_SIZE').
        :return: 'nutrition_score'. Type: String.
        """
        for score in self.api_products[page_n]['products'][product_n]['nutrition_grades_tags']:
            if score[2:]:  # If second letter is true (for "unknown" or "not-applicable")
                nutrition_score = None  # Null
            else:
                nutrition_score = score.upper()
            return nutrition_score


class Exclusive:
    """
    Get rid of duplicated products.
    """

    def __init__(self, s_products):
        self.s_products = s_products

    def duplicate(self):
        """
        Identify duplicated products by name.
        Stock products' Index from previously filtered products.
        :return: 'DUPLICATE_INDEX'. Type: Dict.
        """
        names_list = [self.s_products[i]['name'] for i in range(0, len(self.s_products))]

        for i in range(0, len(self.s_products)):
            if names_list[i] in settings.DUPLICATE_INDEX:
                settings.DUPLICATE_INDEX[names_list[i]].append(i)
            elif names_list.count(names_list[i]) > 1:
                settings.DUPLICATE_INDEX.update({names_list[i]: [i]})

    def recursive(self, key, string):
        """
        Select the more recursive value from given product (param 'key') and category (param 'string').
        :param key: Key from 'DUPLICATE_INDEX'.
        :param string: String to determine which value to search (& filter). Given in 'data.Save.unique_products()'.
        :return: 'unique_value'. Type: Int | String | Dict | List
        """
        if string == 'id':
            unique_value = self.s_products[settings.DUPLICATE_INDEX[key][0]][string]
            return unique_value
        elif string == 'stores':
            unique_value = []
            # Can be done with List Comprehension, but might be harder to read.
            for k in settings.DUPLICATE_INDEX[key]:
                if self.s_products[k][string] is not None:
                    for v in self.s_products[k][string]:
                        if v not in unique_value:
                            unique_value.append(v)
            # If product have no store.
            if not unique_value:
                unique_value = None
            return unique_value
        elif (string == 'allergens') or (string == 'labels'):
            temp_list = {}
            count_value = {}
            unique_value = {}
            for k in settings.DUPLICATE_INDEX[key]:
                for v in self.s_products[k][string]:
                    if v in temp_list:
                        temp_list[v].append(self.s_products[k][string][v])
                    else:
                        temp_list.update({v: [self.s_products[k][string][v]]})
            for k in temp_list:
                for v in temp_list[k]:
                    if v in count_value:
                        count_value[k].append(temp_list[k].count(v))
                    else:
                        count_value.update({k: [temp_list[k].count(v)]})
            for k in count_value:
                unique_value.update({k: temp_list[k][count_value[k].index(max(count_value[k]))]})
            return unique_value
        else:
            temp_list = [self.s_products[k][string] for k in settings.DUPLICATE_INDEX[key]]
            count_list = [temp_list.count(i) for i in temp_list]
            temp_list.reverse()
            count_list.reverse()
            unique_value = temp_list[count_list.index(max(count_list))]
            return unique_value
