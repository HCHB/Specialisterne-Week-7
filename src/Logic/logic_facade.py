from src.project_enums import ObjectTypes, SearchTypes

from src.Data.data_facade import DataFacade

from src.Logic.report_generator import ReportGenerator


class LogicFacade:
    _report_generator: type(ReportGenerator)
    _data_facade: type(DataFacade)

    def __init__(self):
        self._data_facade = DataFacade()
        self._report_generator = ReportGenerator(self._data_facade)

    def search(self, procedure, parameters):
        try:
            parameters = list(parameters.values())
            results = self._data_facade.search(procedure, parameters)
            return results
        except Exception as e:
            return False

    def get_search_parameters(self, procedure):
        try:
            parameters = self._data_facade.get_search_parameters(procedure)
            return parameters
        except Exception as e:
            return False

    def _make_transaction(self, parameters):
        # These checks could also be moved into the database procedure

        item_parameters = self._data_facade.get_search_parameters(SearchTypes.ITEM)
        item_parameters['item_id'] = parameters['item_id']
        item_parameters = list(item_parameters.values())
        items = self._data_facade.search(SearchTypes.ITEM, item_parameters)

        if len(items) > 1:
            return False

        item = items[0]
        amount = parameters['amount']

        try:
            amount = int(amount)
        except Exception as e:
            return False

        if amount < 0 and amount + item.stock < 0:
            return False
        else:
            transaction = self._data_facade.add(ObjectTypes.TRANSACTION, parameters)
            return transaction

    def get_database_object_fields(self, object_type):
        try:
            # TODO could also be used to filter for what fields users are allowed to see
            return self._data_facade.get_database_object_fields(object_type)
        except Exception as e:
            return False

    def add(self, database_object, parameters):
        try:
            if database_object is ObjectTypes.TRANSACTION:
                return self._make_transaction(parameters)

            return self._data_facade.add(database_object, parameters)
        except Exception as e:
            return False

    def update(self, database_object, fields=None):
        try:
            return self._data_facade.update(database_object, fields)
        except Exception as e:
            return False

    def remove(self, database_object):
        try:
            return self._data_facade.remove(database_object)
        except Exception as e:
            return False

    def generate_report(self, report_type, **kwargs):
        try:
            report = self._report_generator.generate_report(report_type, **kwargs)
            return report
        except Exception as e:
            return False

    def get_report_fields(self, report_type):
        try:
            fields = self._report_generator.get_report_fields(report_type)
            return fields
        except Exception as e:
            return False

    def authenticate(self, user, password):
        try:
            return self._data_facade.authenticate(user, password)
        except Exception as e:
            return False

    def logout(self):
        try:
            return self._data_facade.logout()
        except Exception as e:
            return False
