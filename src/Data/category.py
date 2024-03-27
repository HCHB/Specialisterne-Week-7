from src.Data.dataconnection import DataConnection


class Category:
    _id: str
    _name: str
    _description: str

    _data_fields = ['name', 'description']

    def __init__(self, name, description=None, category_id=None):
        self._id = category_id
        self._name = name
        self._description = description

    def add(self):
        command = 'add_category'
        values = [self._name, self._description]

        connection = DataConnection()
        category_id = connection.execute_procedure(command, values)
        self._id = category_id

    def update(self, parameters=None):
        if parameters:
            self._update_properties(parameters)

        command = ('UPDATE Category '
                   'SET name=%(name)s, description = %(description)s '
                   'WHERE category_id = %(id)s')

        values = {
            'name': self._name,
            'description': self._description,
            'id': self._id
        }

        DataConnection().execute_command(command, values)

        return True

    def remove(self):
        command = ('DELETE FROM Category '
                   'WHERE category_id = %(id)s')

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
                f'Description: {self._description}')

    def _update_properties(self, parameters):
        if 'name' in parameters and parameters['name'] is not None:
            self._name = parameters['name']

        if 'description' in parameters and parameters['description'] is not None:
            self._description = parameters['description']

    @property
    def id(self):
        return self._id
