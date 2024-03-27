from src.Data.dataconnection import DataConnection


class Item:
    _id: str
    _name: str
    _description: str
    _category_id: int
    _price: float
    _stock: int
    _stock_target: int

    _data_fields = ['name', 'description', 'category_id', 'price', 'stock', 'stock_target']

    def __init__(self, name, description=None, category_id=None,
                 price=None, stock=None, stock_target=None, item_id=None):
        self._stock = stock
        self._price = price
        self._category_id = category_id
        self._description = description
        self._name = name
        self._id = item_id
        self._stock_target = stock_target

    def add(self):
        command = 'add_item'
        values = [self._name, self._description, self._category_id, self._price, self._stock, self._stock_target]

        connection = DataConnection()
        item_id = connection.execute_procedure(command, values)
        self._id = item_id

    def update(self, parameters=None):
        if parameters:
            self._update_properties(parameters)

        command = ('UPDATE Item '
                   'SET name=%(name)s, '
                   'description = %(description)s, '
                   'category_id = %(category_id)s, '
                   'price = %(price)s, '
                   'stock = %(stock)s, '
                   'stock_target = %(stock_target)s '
                   'WHERE item_id = %(id)s;')

        values = {
            'name': self._name,
            'description': self._description,
            'id': self._id,
            'category_id': self._category_id,
            'price': self._price,
            'stock': self._stock,
            'stock_target': self._stock_target
        }

        DataConnection().execute_command(command, values)

        return True

    def remove(self):
        command = ('DELETE FROM Item '
                   'WHERE item_id = %(id)s')

        values = {
            'id': self._id
        }

        DataConnection().execute_command(command, values)

        return True

    @classmethod
    def get_fields(cls):
        return cls._data_fields

    def __str__(self):
        return (f'ID: {self._id}, '
                f'Name: {self._name}, '
                f'Description: {self._description}, '
                f'Category ID: {self._category_id}, '
                f'Price: {self._price}, '
                f'Stock: {self._stock}, '
                f'Stock Target: {self._stock_target}')

    def _update_properties(self, parameters):
        if 'name' in parameters and parameters['name'] is not None:
            self._name = parameters['name']

        if 'description' in parameters and parameters['description'] is not None:
            self._description = parameters['description']

        if 'category_id' in parameters and parameters['category_id'] is not None:
            self._category_id = parameters['category_id']

        if 'price' in parameters and parameters['price'] is not None:
            self._price = int(parameters['price'])

        if 'stock' in parameters and parameters['stock'] is not None:
            self.stock = int(parameters['stock'])

        if 'stock_target' in parameters and parameters['stock'] is not None:
            self._stock_target = int(parameters['stock'])

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        if stock < 0:
            raise ValueError("Stock can't be negative")

        self._stock = stock


class PrintMedia(Item):
    pass


class Furniture(Item):
    pass


class Vehicle(Item):
    pass
