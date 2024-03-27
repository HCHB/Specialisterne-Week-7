from src.project_enums import ObjectTypes

from src.Data.category import Category
from src.Data.item_factory import ItemFactory
from src.Data.log import Log
from src.Data.transaction import Transaction


class CategoryBuilder:
    @staticmethod
    def build(**kwargs):
        category = Category(**kwargs)
        return category

    @staticmethod
    def get_fields(**kwargs):
        return Category.get_fields()


class TransactionBuilder:
    @staticmethod
    def build(**kwargs):
        transaction = Transaction(**kwargs)
        return transaction

    @staticmethod
    def get_fields(**kwargs):
        return Transaction.get_fields()


class LogBuilder:
    @staticmethod
    def build(**kwargs):
        log = Log(**kwargs)
        return log

    @staticmethod
    def get_fields(**kwargs):
        return Log.get_fields()


class ObjectFactory:
    _builders = {ObjectTypes.ITEM: ItemFactory(),
                 ObjectTypes.CATEGORY: CategoryBuilder(),
                 ObjectTypes.TRANSACTION: TransactionBuilder(),
                 ObjectTypes.LOG: LogBuilder()
                 }

    def build(self, object_type, **kwargs):
        builder = self._decider(object_type)

        new_object = builder.build(**kwargs)

        return new_object

    def _decider(self, object_type):
        builder = self._builders[object_type]
        return builder

    def add_builder(self, object_type, builder):
        if object_type in self._builders:
            raise Exception(f'A builder for {object_type} already exists')

        self._builders[object_type] = builder

    def replace_builder(self, object_type, builder):
        self._builders[object_type] = builder

    def get_object_fields(self, object_type, **kwargs):
        builder = self._decider(object_type)
        return builder.get_fields(**kwargs)
