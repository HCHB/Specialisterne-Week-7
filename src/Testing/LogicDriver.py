from src.project_enums import ObjectTypes, ReportTypes, TransactionTypes, SearchTypes
from src.decorators import print_decorator

from src.Logic.logic_facade import LogicFacade


class LogicDriver:
    def __init__(self):
        self._logic_facade = LogicFacade()
        user = 'hebo_test_admin'
        password = 'test123'
        self._logic_facade.authenticate(user, password)

    def invoke_all_tests(self):
        self._test_get_search_parameters()
        self._test_search()
        self._test_transaction()
        self._test_get_object_fields()
        self._test_add()
        self._test_update()
        self._test_remove()
        self._test_generate_report()

    def _print_objects(self, data_objects):
        for data_object in data_objects:
            print(data_object)

    @print_decorator
    def _test_get_search_parameters(self):
        parameters = self._logic_facade.get_search_parameters(SearchTypes.ITEM)
        print(parameters)
        print()
        parameters = self._logic_facade.get_search_parameters(SearchTypes.LOG)
        print(parameters)
        print()
        parameters = self._logic_facade.get_search_parameters(SearchTypes.CATEGORY)
        print(parameters)
        print()
        parameters = self._logic_facade.get_search_parameters(SearchTypes.TRANSACTION)
        print(parameters)

    @print_decorator
    def _test_search(self):
        parameters = self._logic_facade.get_search_parameters(SearchTypes.ITEM)
        parameters['item_id'] = 1
        data_objects = self._logic_facade.search(SearchTypes.ITEM, parameters)
        self._print_objects(data_objects)

        parameters = self._logic_facade.get_search_parameters(SearchTypes.CATEGORY)
        parameters['category_id'] = 1
        data_objects = self._logic_facade.search(SearchTypes.CATEGORY, parameters)
        self._print_objects(data_objects)

        parameters = self._logic_facade.get_search_parameters(SearchTypes.TRANSACTION)
        parameters['transaction_id'] = 1
        data_objects = self._logic_facade.search(SearchTypes.TRANSACTION, parameters)
        self._print_objects(data_objects)

        parameters = self._logic_facade.get_search_parameters(SearchTypes.LOG)
        parameters['log_id'] = 1
        data_objects = self._logic_facade.search(SearchTypes.LOG, parameters)
        self._print_objects(data_objects)

    @print_decorator
    def _test_transaction(self):
        parameter_item = self._logic_facade.get_search_parameters(SearchTypes.ITEM)
        parameter_transaction = self._logic_facade.get_search_parameters(SearchTypes.TRANSACTION)

        self._print_objects(self._logic_facade.search(SearchTypes.ITEM, parameter_item))
        self._print_objects(self._logic_facade.search(SearchTypes.TRANSACTION, parameter_transaction))

        print()
        self._logic_facade.add(ObjectTypes.TRANSACTION, {'item_id': 1, 'amount': -1, 'transaction_type': TransactionTypes.SALE.value})
        print()

        self._print_objects(self._logic_facade.search(SearchTypes.ITEM, parameter_item))
        self._print_objects(self._logic_facade.search(SearchTypes.TRANSACTION, parameter_transaction))

    @print_decorator
    def _test_get_object_fields(self):
        print(self._logic_facade.get_database_object_fields(ObjectTypes.ITEM))
        print()
        print(self._logic_facade.get_database_object_fields(ObjectTypes.CATEGORY))
        print()
        print(self._logic_facade.get_database_object_fields(ObjectTypes.LOG))
        print()
        print(self._logic_facade.get_database_object_fields(ObjectTypes.TRANSACTION))

    @print_decorator
    def _test_add(self):
        # _data_fields = {'name': , 'description': , 'category': , 'price': , 'stock': , 'stock_target: '}
        # _data_fields = {'name': , 'description': }
        # _data_fields = []
        # _data_fields = {'item_id': , 'amount': , 'transaction_type': }
        parameter_item = self._logic_facade.get_search_parameters(SearchTypes.ITEM)
        parameter_category = self._logic_facade.get_search_parameters(SearchTypes.CATEGORY)
        parameter_transaction = self._logic_facade.get_search_parameters(SearchTypes.TRANSACTION)
        parameter_log = self._logic_facade.get_search_parameters(SearchTypes.LOG)


        self._print_objects(self._logic_facade.search(SearchTypes.ITEM, parameter_item))
        self._logic_facade.add(ObjectTypes.ITEM, {'name': 'paper', 'description': 'for writing', 'category_id': 1, 'price': None, 'stock': None, 'stock_target': None})
        print()
        self._print_objects(self._logic_facade.search(SearchTypes.ITEM, parameter_item))
        print('----------')
        self._print_objects(self._logic_facade.search(SearchTypes.CATEGORY, parameter_category))
        self._logic_facade.add(ObjectTypes.CATEGORY, {'name': 'paper', 'description': 'for writing'})
        print()
        self._print_objects(self._logic_facade.search(SearchTypes.CATEGORY, parameter_category))
        print('----------')
        try:
            self._print_objects(self._logic_facade.search(SearchTypes.TRANSACTION, parameter_transaction))
            self._logic_facade.add(ObjectTypes.TRANSACTION, {'item_id': 1, 'amount': -1, 'transaction_type': TransactionTypes.SALE.value})
            print()
            self._print_objects(self._logic_facade.search(SearchTypes.TRANSACTION, parameter_transaction))
        except Exception as e:
            print(e)
        print('----------')
        try:
            self._print_objects(self._logic_facade.search(SearchTypes.LOG, parameter_log))
            self._logic_facade.add(ObjectTypes.LOG, {})
            print()
            self._print_objects(self._logic_facade.search(SearchTypes.LOG, parameter_log))
        except Exception as e:
            print(e)

    @print_decorator
    def _test_update(self):
        parameters = self._logic_facade.get_search_parameters(SearchTypes.ITEM)
        parameters['item_id'] = 1
        data_object = self._logic_facade.search(SearchTypes.ITEM, parameters)[0]
        print(data_object)
        print()
        data_object.stock = 300
        data_object.update()
        print(self._logic_facade.search(SearchTypes.ITEM, parameters)[0])

    @print_decorator
    def _test_remove(self):
        parameters = self._logic_facade.get_search_parameters(SearchTypes.ITEM)

        self._print_objects(self._logic_facade.search(SearchTypes.ITEM, parameters))
        parameters['item_id'] = 3
        data_object = self._logic_facade.search(SearchTypes.ITEM, parameters)[0]
        print()
        print(data_object)
        data_object.remove()
        print()
        parameters['item_id'] = None
        self._print_objects(self._logic_facade.search(SearchTypes.ITEM, parameters))

    @print_decorator
    def _test_generate_report(self):
        report = self._logic_facade.generate_report(ReportTypes.INVENTORY)
        print(report)
        print()
        report = self._logic_facade.generate_report(ReportTypes.CATEGORY, **{'category_id': 2})
        print(report)
        # report = self._logic_facade.generate_report(ReportTypes.INVENTORY)
        # print(report)
        # report = self._logic_facade.generate_report(ReportTypes.INVENTORY)
        # print(report)


if __name__ == '__main__':
    driver = LogicDriver()
    driver.invoke_all_tests()
