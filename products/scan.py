from products import data, settings, sort

"""
Scan through 'api_products' (from 'apy.Off()') to create 'sorted_products' and 'unique_products'.
"""


class Products:
    """
    Loop X times to call filter / sort algorithm and keep relevant products.
    Then loop X times inside 'DUPLICATE_INDEX' to get unique products only.
    """

    def __init__(self, api_products):
        self.page_n = 0
        self.product_n = 0
        # Init Class
        self.save = data.Save(api_products)
        self.dic = sort.Dictionary(api_products)
        self.excl = sort.Exclusive(self.save.s_products)

    def sorted(self):
        """
        Loop to save relevant products. (Those with a french name, description and 3 categories at least).
        Call data.Save() to save products.
        """
        while self.page_n < settings.PAGE_LIMIT:
            while self.product_n < settings.PAGE_SIZE:
                try:
                    if self.dic.complete(self.page_n, self.product_n):
                        self.save.sorted_product(self.page_n, self.product_n, self.dic.categories, self.dic.length)
                        self.product_n += 1
                    else:
                        self.product_n += 1
                except KeyError:
                    self.product_n += 1
                except IndexError:
                    self.product_n += 1
                self.dic.categories = []
                self.dic.length = -1
            self.product_n = 0
            self.page_n += 1

    def unique(self):
        """
        Call script to identify duplicated products and sort them.
        Save duplicate index to delete them later on.
        """
        self.excl.duplicate()

        for key in settings.DUPLICATE_INDEX:
            self.save.unique_products(key)

        del_list = [v for k in settings.DUPLICATE_INDEX for v in settings.DUPLICATE_INDEX[k]]
        self.save.write(del_list)
