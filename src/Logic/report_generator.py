import copy

from src.project_enums import ReportTypes, ObjectTypes, SearchTypes


class ReportGenerator:

    def __init__(self, data_facade):
        self._generators = {ReportTypes.INVENTORY: {'procedure': self._complete_inventory,
                                                    'parameters': {}
                                                    },
                            ReportTypes.CATEGORIES: {'procedure': self._inventory_by_category,
                                                     'parameters': {}
                                                     },
                            ReportTypes.CATEGORY: {'procedure': self._category_inventory,
                                                   'parameters': {'category_id': None}
                                                   },
                            ReportTypes.LOW_STOCK: {'procedure': self._low_stock,
                                                    'parameters': {'category_id': None}
                                                    },
                            ReportTypes.INCOMPLETE_ITEMS: {'procedure': self._incomplete_items,
                                                           'parameters': {}
                                                           },
                            ReportTypes.INCOMPLETE_CATEGORIES: {'procedure': self._incomplete_categories,
                                                                'parameters': {}
                                                                }
                            }

        self._data_facade = data_facade

    def generate_report(self, report_type, **kwargs):
        generator = self._decider(report_type, 'procedure')

        report = generator(**kwargs)

        return report

    def get_report_fields(self, report_type):
        parameters = self._decider(report_type, 'parameters')
        return copy.deepcopy(parameters)

    def _decider(self, report_type, item):
        generator = self._generators[report_type][item]
        return generator

    def add_generator(self, report_type, generator):
        if report_type in self._generators:
            raise Exception(f'A generator for {report_type} already exists')

        self._generators[report_type] = generator

    def replace_generator(self, report_type, generator):
        self._generators[report_type] = generator

    def _complete_inventory(self, **kwargs):
        parameters = self._data_facade.get_search_parameters(SearchTypes.ITEM)

        item_parameters = list(parameters.values())

        items = self._data_facade.search(SearchTypes.ITEM, item_parameters)

        report_string = 'Complete Inventory Report:\n'
        report_string += 'Items:'
        for item in items:
            report_string += f'\n\t{item}'

        return report_string

    def _inventory_by_category(self, **kwargs):
        report_string = 'Inventory Report by category:\n'

        parameters = self._data_facade.get_search_parameters(SearchTypes.CATEGORY)
        category_parameters = list(parameters.values())

        categories = self._data_facade.search(SearchTypes.CATEGORY, category_parameters)

        for category in categories:
            report_string += f'\tCategory: {category}\n'

            parameters = self._data_facade.get_search_parameters(SearchTypes.ITEM)
            parameters['cat_id'] = category.id
            item_parameters = list(parameters.values())

            items = self._data_facade.search(SearchTypes.ITEM, item_parameters)

            report_string += '\tItems:\n'
            for item in items:
                report_string += f'\t\t{item}\n'
            report_string += '\n'

        return report_string

    def _category_inventory(self, **kwargs):
        report_string = 'Category Inventory Report:\n'

        parameters = self._data_facade.get_search_parameters(SearchTypes.CATEGORY)
        parameters['category_id'] = kwargs['category_id']
        category_parameters = list(parameters.values())

        categories = self._data_facade.search(SearchTypes.CATEGORY, category_parameters)

        for category in categories:
            parameters = self._data_facade.get_search_parameters(SearchTypes.ITEM)
            parameters['cat_id'] = category.id
            item_parameters = list(parameters.values())

            items = self._data_facade.search(SearchTypes.ITEM, item_parameters)

            report_string += '\tItems:\n'
            for item in items:
                report_string += f'\t\t{item}\n'
            report_string += '\n'

        return report_string

    def _low_stock(self, **kwargs):
        parameters = self._data_facade.get_search_parameters(SearchTypes.LOW_STOCK)
        parameters['category_id'] = kwargs['category_id']
        item_parameters = list(parameters.values())

        items = self._data_facade.search(SearchTypes.LOW_STOCK, item_parameters)

        report_string = 'Items with low stock report:'
        for item in items:
            report_string += f'\n\t{item}'

        return report_string

    def _incomplete_items(self, **kwargs):
        parameters = self._data_facade.get_search_parameters(SearchTypes.ITEM_NULL)

        item_parameters = list(parameters.values())

        items = self._data_facade.search(SearchTypes.ITEM_NULL, item_parameters)

        report_string = 'Items with missing fields:'
        for item in items:
            report_string += f'\n\t{item}'

        return report_string

    def _incomplete_categories(self, **kwargs):
        parameters = self._data_facade.get_search_parameters(SearchTypes.CATEGORY_NULL)

        item_parameters = list(parameters.values())

        items = self._data_facade.search(SearchTypes.CATEGORY_NULL, item_parameters)

        report_string = 'Categories with missing fields:'
        for item in items:
            report_string += f'\n\t{item}'

        return report_string


if __name__ == "__main__":
    from data_facade import DataFacade

    data = DataFacade()
    data.authenticate('hebo_test_admin', 'test123')
    generator = ReportGenerator(data)

    print(generator.get_report_fields(ReportTypes.INVENTORY))
    print(generator.get_report_fields(ReportTypes.CATEGORIES))
    print(generator.get_report_fields(ReportTypes.CATEGORY))

    report = generator.generate_report(ReportTypes.CATEGORIES)
    print(report)

    param = generator.get_report_fields(ReportTypes.CATEGORY)
    param['category_id'] = 2

    report = generator.generate_report(ReportTypes.CATEGORY, **param)
    print(report)