import copy

from src.project_enums import ObjectTypes, SearchTypes

from src.Data.object_factory import ObjectFactory


class Inventory:
    def __init__(self, data_connection):
        self._data_connection = data_connection
    _procedures = {
        SearchTypes.ITEM: {'procedure': 'search_item',
                           'parameters': {'item_id': None,
                                          'item_name': None,
                                          'item_description': None,
                                          'cat_id': None,
                                          'item_price': None,
                                          'item_stock': None,
                                          'item_stock_target': None},
                           'object_type': ObjectTypes.ITEM
                           },
        SearchTypes.CATEGORY: {'procedure': 'search_category',
                               'parameters': {'category_id': None,
                                              'name': None,
                                              'description': None},
                               'object_type': ObjectTypes.CATEGORY
                               },
        SearchTypes.TRANSACTION: {'procedure': 'search_transaction',
                                  'parameters': {'transaction_id': None,
                                                 'item_id': None,
                                                 'transaction_time': None,
                                                 'amount': None,
                                                 'transaction_type': None},
                                  'object_type': ObjectTypes.TRANSACTION
                                  },
        SearchTypes.LOG: {'procedure': 'search_log',
                          'parameters': {'log_id': None,
                                         'event_name': None,
                                         'table_name': None,
                                         'user_name': None,
                                         'performed': None},
                          'object_type': ObjectTypes.LOG
                          },
        SearchTypes.ITEM_NULL: {'procedure': 'search_item_nulls',
                                'parameters': {},
                                'object_type': ObjectTypes.ITEM
                                },
        SearchTypes.CATEGORY_NULL: {'procedure': 'search_category_nulls',
                                    'parameters': {},
                                    'object_type': ObjectTypes.CATEGORY
                                    },
        SearchTypes.LOW_STOCK: {'procedure': 'search_low_stock',
                                'parameters': {'category_id': None},
                                'object_type': ObjectTypes.ITEM
                                },
    }


    def search(self, procedure, args):
        command = self._decider(procedure, 'procedure')
        values = [*args]

        results = self._data_connection.execute_procedure(command, values)

        factory = ObjectFactory()
        objects = []

        if type(results) is not list:
            results = [results]

        item_type = self._get_return_type(procedure)

        for result in results:
            new_object = factory.build(item_type, **result)
            objects.append(new_object)

        return objects

    def get_search_parameters(self, procedure):
        parameters = self._decider(procedure, 'parameters')
        return copy.deepcopy(parameters)

    def _decider(self, procedure, item):
        command = self._procedures[procedure][item]
        return command

    def _get_return_type(self, procedure):  # TODO if more than simple table search
        object_type = self._decider(procedure, 'object_type')
        return object_type
