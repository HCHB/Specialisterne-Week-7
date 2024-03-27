import os
from getpass import getpass

from src.project_enums import ReportTypes, ObjectTypes, SearchTypes
from src.Logic.logic_facade import LogicFacade


class UIMenu:
    _menu_name: str = 'Generic Menu'

    def __init__(self):
        self._reset_menu()

    def _reset_menu(self):
        self._return_value = None
        self._status_message = ''

        self._item_type = ''
        self._items = []

        self._fields = {}

        self.choices = {
            '1': self._return
        }

        self.print_statements = [
            '1. Return'
        ]

    def _display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self._menu_name}:")

        if self._items:
            print()
            print(f'{self._item_type}:')
            for count, item in enumerate(self._items):
                print(f'\t{count}: {item}')

        if self._status_message:
            print()
            print(self._status_message)

        if self._fields:
            print()
            for field, value in self._fields.items():
                print(f'{field}: {value}')

        print()
        for choice in self.print_statements:
            print(choice)

    def _return(self):
        print('Returning from menu')
        # self._reset_menu()
        return False

    def _set_field_function(self, attribute_name, default_status=''):
        def set_field():
            self._status_message = default_status

            self._fields[attribute_name] = input().strip()
            return True

        return set_field

    def run(self):
        continue_menu = True
        while continue_menu:
            self._display_menu()
            choice = input("Enter your choice: ")

            if choice in self.choices:
                continue_menu = self.choices[choice]()
            else:
                self._status_message = "Invalid choice. Please try again."

        return self._return_value


class UpdateMenu(UIMenu):

    def __init__(self, logic_facade, object_type, data_object):
        self._menu_name = f'Update {object_type.value} menu'
        self._logic_facade = logic_facade
        self._type = object_type
        self._data_object = data_object
        super().__init__()

        self._display_menu = super()._display_menu

    def _reset_menu(self):
        super()._reset_menu()

        self._status_message = f'Selected: {self._data_object}'

        parameters = self._logic_facade.get_database_object_fields(self._type)

        if not parameters:
            self._status_message = 'No object fields found'
            parameters = []

        for parameter in parameters:
            self._fields[parameter] = None

        self.choices = {}
        self.print_statements = []

        number = 0
        for number, field in enumerate(self._fields):
            number_string = str(number + 1)
            self.choices[number_string] = self._set_field_function(field, self._status_message)
            self.print_statements.append(f'{number_string}. Enter {field}')
        number += 1

        number += 1
        self.choices[str(number)] = self._update
        self.print_statements.append(f'{number}. Update')

        number += 1
        self.choices[str(number)] = self._reset_menu
        self.print_statements.append(f'{number}. Reset menu')

        number += 1
        self.choices[str(number)] = self._return
        self.print_statements.append(f'{number}. Return')

        return True

    def _update(self):
        success = self._logic_facade.update(self._data_object, self._fields)

        if success:
            self._return_value = True
            return False
        else:
            self._status_message += f'\nUpdate failed'
            return True


class AddMenu(UIMenu):

    def __init__(self, logic_facade, object_type, default_status=''):
        self._logic_facade = logic_facade
        self._type = object_type
        self._default_status = default_status

        self._menu_name = f'Add {object_type.value} menu'
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self._status_message = self._default_status

        parameters = self._logic_facade.get_database_object_fields(self._type)

        if not parameters:
            self._status_message = 'No object fields found'
            parameters = []

        for parameter in parameters:
            self._fields[parameter] = None

        self.choices = {}
        self.print_statements = []

        number = 0
        for number, field in enumerate(self._fields):
            number_string = str(number + 1)
            self.choices[number_string] = self._set_field_function(field, default_status=self._default_status)
            self.print_statements.append(f'{number_string}. Enter {field}')
        number += 1

        number += 1
        self.choices[str(number)] = self._add
        self.print_statements.append(f'{number}. Add')

        number += 1
        self.choices[str(number)] = self._reset_menu
        self.print_statements.append(f'{number}. Reset menu')

        number += 1
        self.choices[str(number)] = self._return
        self.print_statements.append(f'{number}. Return')

        return True

    def _add(self):
        item = self._logic_facade.add(self._type, self._fields)

        if item:
            self._return_value = f'Item was added'
            return False
        else:
            self._status_message += f'\nAdd failed'
            return True


class SearchMenu(UIMenu):

    def __init__(self, logic_facade, search_type, selectable=True):
        self._logic_facade = logic_facade
        self._type = search_type
        self._selectable = selectable
        super().__init__()
        self._menu_name = f'{search_type.value} Menu'

    def _reset_menu(self):
        super()._reset_menu()

        self._item_type = self._type.value
        fields = self._logic_facade.get_search_parameters(self._type)

        if not fields:
            self._status_message = 'No search fields found'
            fields = {}
        self._fields = fields

        self.choices = {}
        self.print_statements = []

        number = 0
        for number, field in enumerate(self._fields):
            number_string = str(number + 1)
            self.choices[number_string] = self._set_field_function(field)
            self.print_statements.append(f'{number_string}. Enter {field}')
        number += 1

        number += 1
        self.choices[str(number)] = self._search
        self.print_statements.append(f'{number}. Search')

        number += 1
        self.choices[str(number)] = self._reset_menu
        self.print_statements.append(f'{number}. Reset menu')

        if self._selectable:
            number += 1
            self.choices[str(number)] = self._select
            self.print_statements.append(f'{number}. Select')

        number += 1
        self.choices[str(number)] = self._return
        self.print_statements.append(f'{number}. Return')

        return True

    def _search(self):
        items = self._logic_facade.search(self._type, self._fields)
        if not items:
            self._status_message = 'Search failed'
            items = []
        else:
            self._status_message = ''

        self._items = items

        return True

    def _select(self):
        number = input().strip()

        try:
            number = int(number)
            self._return_value = self._items[number]
            self._status_message = f'Selected: {self._return_value}'
            return False
        except Exception as e:
            self._status_message = "Invalid choice. Please try again."
            return True


class LoginMenu(UIMenu):
    _menu_name: str = 'Login Menu'

    _username: str = ''
    _password: str = ''
    _status_message: str = ''

    def __init__(self):
        self._logic_facade = LogicFacade()
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self._username = ''
        self._password = ''

        self._fields = {'Username': '',
                        'Password': ''}

        self.choices = {
            '1': self._enter_username,
            '2': self._enter_password,
            '3': self._login,
            '4': self._return
        }

        self.print_statements = [
            '1. Enter username',
            '2. Enter password',
            '3. Login',
            '4. Exit'
        ]

    def _enter_username(self):
        self._status_message = ''
        self._username = input().strip()
        self._fields['Username'] = self._username
        return True

    def _enter_password(self):
        self._status_message = ''
        self._password = getpass('').strip()
        self._fields['Password'] = len(self._password)*'*'
        return True

    def _login(self):
        success = self._logic_facade.authenticate(self._username, self._password)

        if success:
            self._status_message = ''
            submenu = MainMenu(self._logic_facade)
            submenu.run()
            self._reset_menu()
            return True
        else:
            self._status_message = 'Invalid username or password'
            return True


class MainMenu(UIMenu):
    _menu_name: str = 'Main Menu'

    def __init__(self, logic_facade):
        self._logic_facade = logic_facade
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self.choices = {
            '1': self._reports,
            '2': self._items_menu,
            '3': self._categories,
            '4': self._transactions,
            '5': self._logs,
            '6': self._logout
        }

        self.print_statements = [
            '1. Reports',
            '2. Items',
            '3. Categories',
            '4. Transactions',
            '5. Log',
            '6. Logout'
        ]

    def _reports(self):
        submenu = ReportMenu(self._logic_facade)
        submenu.run()
        return True

    def _items_menu(self):
        submenu = ItemMenu(self._logic_facade)
        submenu.run()
        return True

    def _categories(self):
        submenu = CategoryMenu(self._logic_facade)
        submenu.run()
        return True

    def _transactions(self):
        submenu = TransactionMenu(self._logic_facade)
        submenu.run()
        return True

    def _logs(self):
        submenu = SearchMenu(self._logic_facade, SearchTypes.LOG, selectable=False)
        submenu.run()

        return True

    def _logout(self):
        self._logic_facade.logout()
        return False


class ItemMenu(UIMenu):
    _menu_name: str = 'Item Menu'

    def __init__(self, logic_facade):
        self._logic_facade = logic_facade
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self._selected_item = None

        self.choices = {
            '1': self._search,
            '2': self._add,
            '3': self._update,
            '4': self._remove,
            '5': self._return
        }

        self.print_statements = [
            '1. Search',
            '2. Add',
            '3. Update',
            '4. Remove',
            '5. Return'
        ]

    def _search(self):
        submenu = SearchMenu(self._logic_facade, SearchTypes.ITEM)
        item = submenu.run()

        self._reset_menu()

        self._selected_item = item
        self._status_message = f'Selected: {self._selected_item}'

        return True

    def _update(self):
        if not self._selected_item:
            self._status_message = 'Select an item to update'
            return True

        submenu = UpdateMenu(self._logic_facade, ObjectTypes.ITEM, self._selected_item)
        success = submenu.run()
        item = self._selected_item

        self._reset_menu()

        if success:
            self._status_message = f'{item}\nwas updated'
        else:
            self._status_message = f'Update failed'

        return True

    def _add(self):
        submenu = AddMenu(self._logic_facade, ObjectTypes.ITEM)
        message = submenu.run()

        self._reset_menu()

        self._status_message = message
        return True

    def _remove(self):
        if not self._selected_item:
            self._status_message = 'Select an item to remove'
            return True

        success = self._logic_facade.remove(self._selected_item)
        item = self._selected_item

        self._reset_menu()

        if success:
            self._status_message = f'{item}\n was removed'
        else:
            self._status_message = f'Remove failed'

        return True


class CategoryMenu(UIMenu):
    _menu_name: str = 'Category Menu'

    def __init__(self, logic_facade):
        self._logic_facade = logic_facade
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self._selected_item = None

        self.choices = {
            '1': self._search,
            '2': self._add,
            '3': self._update,
            '4': self._remove,
            '5': self._return
        }

        self.print_statements = [
            '1. Search',
            '2. Add',
            '3. Update',
            '4. Remove',
            '5. Return'
        ]

    def _search(self):
        submenu = SearchMenu(self._logic_facade, SearchTypes.CATEGORY)
        item = submenu.run()

        self._reset_menu()

        self._selected_item = item
        self._status_message = f'Selected: {self._selected_item}'

        return True

    def _update(self):
        if not self._selected_item:
            self._status_message = 'Select an item to update'
            return True

        submenu = UpdateMenu(self._logic_facade, ObjectTypes.CATEGORY, self._selected_item)
        success = submenu.run()
        item = self._selected_item

        self._reset_menu()

        if success:
            self._status_message = f'{item}\nwas updated'
        else:
            self._status_message = f'Update failed'

        return True

    def _add(self):
        submenu = AddMenu(self._logic_facade, ObjectTypes.CATEGORY)
        message = submenu.run()

        self._reset_menu()

        self._status_message = message
        return True

    def _remove(self):
        if not self._selected_item:
            self._status_message = 'Select an item to remove'
            return True

        success = self._logic_facade.remove(self._selected_item)
        item = self._selected_item

        self._reset_menu()

        if success:
            self._status_message = f'{item}\n was removed'
        else:
            self._status_message = f'Remove failed'

        return True


class TransactionMenu(UIMenu):
    _menu_name: str = 'Transaction Menu'

    def __init__(self, logic_facade):
        self._logic_facade = logic_facade
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self._selected_item = None

        self.choices = {
            '1': self._search_transaction,
            '2': self._search_item,
            '3': self._add,
            '4': self._return
        }

        self.print_statements = [
            '1. Search',
            '2. Find item',
            '3. Add',
            '4. Return'
        ]

    def _search_transaction(self):
        submenu = SearchMenu(self._logic_facade, SearchTypes.TRANSACTION, selectable=False)
        submenu.run()

        self._reset_menu()

        return True

    def _search_item(self):
        submenu = SearchMenu(self._logic_facade, SearchTypes.ITEM)
        item = submenu.run()

        self._reset_menu()

        self._selected_item = item
        self._status_message = f'Selected: {self._selected_item}'

        return True

    def _add(self):
        if not self._selected_item:
            self._status_message = 'Select an item to make a transaction'
            return True

        submenu = AddMenu(self._logic_facade, ObjectTypes.TRANSACTION, default_status=str(self._selected_item))
        message = submenu.run()

        self._reset_menu()

        self._status_message = message
        return True


class ReportMenu(UIMenu):
    _menu_name: str = 'Reports Menu'

    def __init__(self, logic_facade):
        self._logic_facade = logic_facade
        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self.choices = {
            '1': self._complete_inventory,
            '2': self._inventory_by_category,
            '3': self._category_inventory,
            '4': self._low_stock,
            '5': self._incomplete_items,
            '6': self._incomplete_categories,
            '7': self._return
        }

        self.print_statements = [
            '1. Complete Inventory',
            '2. Inventory by category',
            '3. Category inventory',
            '4. Low stock items',
            '5. Incomplete items',
            '6. Incomplete categories',
            '7. Return'
        ]

    def _complete_inventory(self):
        report = self._logic_facade.generate_report(ReportTypes.INVENTORY)
        if not report:
            self._status_message = 'Report generation failed'
            report = ''

        self._status_message = report
        return True

    def _inventory_by_category(self):
        report = self._logic_facade.generate_report(ReportTypes.CATEGORIES)
        if not report:
            self._status_message = 'Report generation failed'
            report = ''

        self._status_message = report
        return True

    def _category_inventory(self):
        parameters = self._logic_facade.get_report_fields(ReportTypes.CATEGORY)
        submenu = ParameterMenu(parameters)
        parameters = submenu.run()

        report = self._logic_facade.generate_report(ReportTypes.CATEGORY, **parameters)
        if not report:
            self._status_message = 'Report generation failed'
            report = ''

        self._status_message = report
        return True

    def _low_stock(self):
        parameters = self._logic_facade.get_report_fields(ReportTypes.LOW_STOCK)
        submenu = ParameterMenu(parameters)
        parameters = submenu.run()

        report = self._logic_facade.generate_report(ReportTypes.LOW_STOCK, **parameters)
        if not report:
            self._status_message = 'Report generation failed'
            report = ''

        self._status_message = report
        return True

    def _incomplete_items(self):
        report = self._logic_facade.generate_report(ReportTypes.INCOMPLETE_ITEMS)
        if not report:
            self._status_message = 'Report generation failed'
            report = ''

        self._status_message = report
        return True

    def _incomplete_categories(self):
        report = self._logic_facade.generate_report(ReportTypes.INCOMPLETE_CATEGORIES, **{})
        if not report:
            self._status_message = 'Report generation failed'
            report = ''

        self._status_message = report
        return True


class ParameterMenu(UIMenu):

    def __init__(self, parameters):
        self._parameters = parameters
        self._menu_name = f'Add parameter menu'
        self._return_value = parameters

        super().__init__()

    def _reset_menu(self):
        super()._reset_menu()

        self._return_value = self._fields

        if not self._parameters:
            self._status_message = 'No object fields found'
            self._fields = {}

        for field in self._parameters:
            self._fields[field] = None

        self.choices = {}
        self.print_statements = []

        number = 0
        for number, field in enumerate(self._fields):
            number_string = str(number + 1)
            self.choices[number_string] = self._set_field_function(field)
            self.print_statements.append(f'{number_string}. Enter {field}')
        number += 1

        number += 1
        self.choices[str(number)] = self._reset_menu
        self.print_statements.append(f'{number}. Reset menu')

        number += 1
        self.choices[str(number)] = self._return
        self.print_statements.append(f'{number}. Return')

        return True


if __name__ == "__main__":
    # TODO can see and start everything (will be denied in the data layer or in the database
    menu = LoginMenu()
    menu.run()
