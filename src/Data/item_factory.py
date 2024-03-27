from src.project_enums import Categories

from src.Data.item import PrintMedia, Furniture, Vehicle, Item


class ItemFactory:
    _builders = {Categories.PRINT: PrintMedia,
                 Categories.FURNITURE: Furniture,
                 Categories.VEHICLE: Vehicle,
                 Categories.MISCELLANEOUS: Item
                 }

    def build(self, **kwargs):
        if 'category_id' in kwargs:
            category_id = kwargs['category_id']
        else:
            category_id = 0

        builder = self._decider(category_id)

        # category = ObjectFactory().build(ObjectTypes.CATEGORY, **kwargs)  # TODO

        new_object = builder(**kwargs)

        return new_object

    def _decider(self, Category_id):
        item_type = Categories(Category_id)

        if item_type not in self._builders:
            item_type = Categories.MISCELLANEOUS

        builder = self._builders[item_type]
        return builder

    def add_builder(self, item_type, builder):
        if item_type in self._builders:
            raise Exception(f'A builder for {item_type} already exists')

        self._builders[item_type] = builder

    def replace_builder(self, item_type, builder):
        self._builders[item_type] = builder

    def get_fields(self, **kwargs):
        if 'category_id' in kwargs:
            category_id = kwargs['category_id']
        else:
            category_id = 0

        builder = self._decider(category_id)
        return builder.get_fields()
