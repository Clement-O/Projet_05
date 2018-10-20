import openfoodfacts

from products import settings

"""
Get data from OpenFoodFacts API.
"""


class Off:
    """
    Query API following parameter in 'settings.py'.
    Calculate how many queries (/pages) should be done.
    Stock data.
    """

    def __init__(self):
        self.api_products = []
        self.result = []

    def query(self, page):
        """
        Get OpenFoodFacts products.
        :param page: Page Number. 1 to .. Max pages calculated in 'page_limit()'.
        :return: Products searched with parameters. Type: List.
                (Default parameters: COUNTRY = France , STATE = Complete , PAGE_SIZE = 1000).
        """
        self.result = openfoodfacts.products.advanced_search({
            "search_terms": "",
            "tagtype_0": "countries",
            "tag_contains_0": "contains",
            "tag_0": settings.COUNTRY,
            "tagtype_1": "states",
            "tag_contains_1": "contains",
            "tag_1": settings.STATE,
            "page": page,
            "page_size": settings.PAGE_SIZE,
            "json": "1"
        })
        return self.result

    def page_limit(self):
        """
        Launch 'query(page=1)' to know how many products can be obtained.
        Calculate how many pages will be needed to get every products (Default PAGE_SIZE = 1000).
        :return: 'PAGE_LIMIT'. Type: Int.
        """
        settings.PRODUCTS_COUNT = self.query(1)['count']  # Get product count from "count" dictionary.
        settings.PAGE_LIMIT = (settings.PRODUCTS_COUNT // settings.PAGE_SIZE) + 1

    def raw_data(self):
        """
        Launch 'query(page)' until 'page' is superior to 'PAGE_LIMIT'.
        :return: Every products fetched (saved in 'self.api_products'). Type: List.
        """
        page = 1
        while page <= settings.PAGE_LIMIT:
            self.api_products.append(self.query(page))  # Append query(page) to self.raw_data
            print(f'Page {str(page)} over {str(settings.PAGE_LIMIT)} fetched !')
            page += 1
