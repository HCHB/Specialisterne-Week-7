from enum import Enum


class ObjectTypes(Enum):
    ITEM = 'Item'
    CATEGORY = 'Category'
    TRANSACTION = 'Transaction'
    LOG = 'Log'


class Categories(Enum):
    MISCELLANEOUS = 1
    PRINT = 2
    FURNITURE = 3
    VEHICLE = 4

    @classmethod
    def _missing_(cls, value):
        return cls.MISCELLANEOUS


class TransactionTypes(Enum):
    SALE = 'sale'
    BUY = 'buy'
    MANUAL = 'manual'
    DESTROY = 'destroy'


class ReportTypes(Enum):
    INVENTORY = 'inventory'
    CATEGORIES = 'categories'
    CATEGORY = 'category'
    LOW_STOCK = 'low stock'
    INCOMPLETE_ITEMS = 'incomplete items'
    INCOMPLETE_CATEGORIES = 'incomplete categories'


class SearchTypes(Enum):
    ITEM = 'Item'
    CATEGORY = 'Category'
    TRANSACTION = 'Transaction'
    LOG = 'Log'
    ITEM_NULL = 'Item null'
    CATEGORY_NULL = 'Category null'
    LOW_STOCK = 'Low stock'
