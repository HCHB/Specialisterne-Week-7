from src.decorators import singleton

from src.Data.dataconnection import DataConnection
from src.Data.inventory import Inventory
from src.Data.object_factory import ObjectFactory


# @singleton
class DataFacade:
    _inventory: type(Inventory)
    _object_factory: type(ObjectFactory)
    _data_connection: type(DataConnection)

    def __init__(self):
        self._object_factory = ObjectFactory()
        self._data_connection = DataConnection(database_name='hebo_week_7')
        self._inventory = Inventory(self._data_connection)

    def search(self, procedure, parameters):
        results = self._inventory.search(procedure, parameters)
        return results

    def get_search_parameters(self, procedure):
        parameters = self._inventory.get_search_parameters(procedure)
        return parameters

    def get_database_object_fields(self, object_type):
        fields = self._object_factory.get_object_fields(object_type, **{})
        return fields

    def add(self, object_type, database_object_parameters: dict):
        object = self._object_factory.build(object_type, **database_object_parameters)
        object.add()
        return object

    def update(self, database_object, fields=None):
        return database_object.update(fields)

    def remove(self, database_object):
        return database_object.remove()

    def authenticate(self, user, password):
        return self._data_connection.authenticate(user, password)

    def logout(self):
        return self._data_connection.logout()
