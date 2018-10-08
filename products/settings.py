
# CONSTANT #
COUNTRY = 'france'      # Change this to modify products' country. In lower case & in english.
STATE = 'complete'      # Change this to modify products' states. In lower case: complete, to-be-completed.
PAGE_SIZE = 1000        # Change this to modify the quantity of products fetched by page.
PRODUCTS_COUNT = 0      # Temporary value. Set in 'products.api.Off.raw_data.page_limit()'.
PAGE_LIMIT = 0          # Temporary value. Set in 'products.api.Off.raw_data.page_limit()'.
DUPLICATE_INDEX = {}    # Temporary value. Set in 'products.sort.Exclusive.duplicate()'.

# Change this to modify products' allergen. In lower case & in english.
ALLERGEN_LIST = [
    'milk',
    'gluten'
]

# Change this to modify products' label. In lower case & in english.
LABEL_LIST = [
    "halal",
    "kosher",
    "organic",
    "vegetarian"
]

# Change this to modify products' store. In french & capitalize every word.
STORE_LIST = [
    'Aldi',
    'Auchan',
    'Biocoop',
    'Carrefour',
    'Casino',
    'Cora',
    'Franprix',
    'Intermarché',
    'Leader Price',
    'Leclerc',
    'Lidl',
    'Magasins U',
    'Monoprix',
    'Picard'
]
