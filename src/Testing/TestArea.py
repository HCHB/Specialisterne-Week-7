# from datetime import date
from pprint import pprint
import mysql.connector

from src.decorators import print_decorator

user = 'hebo_test_user'
password = 'test123'
user = 'hebo_test_admin'
password = 'test123'


@print_decorator
def test_database_insert():
    with (mysql.connector.connect(user=user, password=password, host='localhost', database='hebo_week_7') as connection):
        with connection.cursor(prepared=True) as cursor:
            for i in range(10):
                insert_string = "INSERT INTO item (name) VALUES(%s)"
                insert_string2 = "INSERT INTO item (name) VALUES(%(value1)s)"
                insert_values = [
                    'there',
                ]
                insert_values2 = {
                    'value1': ';DROP TABLE item'
                }
                # command = cursor.execute(insert_string, insert_values)
                command = cursor.execute(insert_string2, insert_values2)
                result = cursor.fetchone() # None
                results = cursor.fetchall() # []
                while result:
                    pprint(result)
                    result = cursor.fetchone()
            # time = datetime(2015, 6, 30, 18, 5, 30)
            # connection.rollback()
            connection.commit()


@print_decorator
def test_database_read():
    with (mysql.connector.connect(user=user, password=password, host='localhost', database='hebo_week_7') as connection):
        with connection.cursor(prepared=True) as cursor:
            command = cursor.execute("SELECT * FROM item")
            result = cursor.fetchone() # (item1)
            # results = cursor.fetchall() # [(item1). (item2), ..., (item3)]
            while result:
                pprint(result)
                result = cursor.fetchone()
            connection.commit()


@print_decorator
def test_stored_procedure_call_insert():
    with (mysql.connector.connect(user=user, password=password, host='localhost', database='hebo_week_7') as connection):
        with connection.cursor() as cursor:
            for i in range(10):
                item_id: int = 0
                name = f';DROP TABLE item;'
                command = cursor.callproc("add_item", [name, None, None, None, None, None])
                stored = cursor.stored_results()
                result_sets = [r.fetchall() for r in stored]  # [[(id)]]

                print(f'{result_sets[0][0][0]} - {command}')

            connection.commit()
        print('Done printing')


@print_decorator
def test_stored_procedure_call_all_items():
    with (mysql.connector.connect(user=user, password=password, host='localhost', database='hebo_week_7') as connection):
        with connection.cursor(dictionary=True) as cursor:
            command = cursor.callproc("search_item", (None, None, None, None, None, None, None))

            stored = cursor.stored_results()
            result_sets = [r.fetchall() for r in stored] # [[(item1). (item2), ..., (item3)]]

            for count1, results in enumerate(result_sets):
                for count2, result in enumerate(results):
                    first = next(iter(result.values()))

                    print(f'{count1}-{count2}: {first} - {result}')

            print('Done printing')


@print_decorator
def test_stored_procedure_call_search_category():
    with (mysql.connector.connect(user=user, password=password, host='localhost', database='hebo_week_7') as connection):
        with connection.cursor() as cursor:
            command = cursor.callproc("search_category", (None, 'bo', None))

            stored = cursor.stored_results()
            result_sets = [r.fetchall() for r in stored]  # [[(item1). (item2), ..., (item3)]]

            for count1, results in enumerate(result_sets):
                for count2, result in enumerate(results):
                    print(f'{count1}-{count2}: {result}')

            print('Done printing')


@print_decorator
def test_repr_vs_str():
    class A:
        val = 'value a'

    class B:
        val = 'value b'

        def __str__(self):
            return f'val: {self.val}'

    a = A()
    b = B()

    print(a)
    print(repr(a))

    print(b)
    print(repr(b))


@print_decorator
def test_strong_typing():
    a: int = 5
    b: str = '5'

    try:
        a = b
        print(type(a))
        print('violated type suggestion')
    except Exception as exception:
        print(exception)

    class A:
        val1: int
        val2: str

        def __init__(self, val1: int, val2: str) -> None:
            self.val1 = val1
            self.val2 = val2

        def to_string(self) -> str:
            return f'{self.val1} {self.val2}'

    c = A(1, '5')
    print(c)
    print(c.to_string())

    c = A(1, 5)
    print(type(c.val2))


@print_decorator
def test_import():
    import sys
    for path in sys.path:
        print(path)

    from src.Testing.package2.module2 import ClassName2

    test = ClassName2()
    test.import_print()

    # UserMenu().run()


@print_decorator
def test_parameter_to_kwarg():
    def k(e, *args, a='a', **kwargs):
        print(e)
        print(a)
        print(args)
        print(kwargs)
        print(kwargs.values())
        val = kwargs.values()
        val2 = kwargs.items()
        val3 = kwargs.keys()
        val4 = list(val)

        print()


    kw = {
        'c': 2,
        'f': 5,
        'h': 3,
        'o': 9,
        'q': 2,
        'b': 1,
        't': 6,
        'y': 4
    }
    k(1, 2, 3, b='b', c='c')
    k('e', a='a', **kw)


@print_decorator
def test_enum_creation():
    from enum import Enum
    class A(Enum):
        A = 'a'
        B = 'b'
        C = 'c'
        D = 'd'

        @classmethod
        def _missing_(cls, value):
            return cls.A

    a = A.A
    b = A.B

    c = A('c')
    e = A('e')
    print('end')


@print_decorator
def test_return_values():
    def a_f():
        return tuple([1, 2, 3])

    print(type([]))
    print(type(()))
    e = a_f()
    a, b = e[0], e[1]
    c = a_f()
    print(a)
    print(b)
    print(c)
    print()

@print_decorator
def test_enumerate_dict():
    a = {'a': '1', 'b': '2'}

    number = 5
    for number, field in enumerate(a):
        print(f'{number} - {field}')

    print(number)

if __name__ == '__main__':
    # try:
    #     test_database_insert()
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     test_database_read()
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     test_stored_procedure_call_insert()
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     test_stored_procedure_call_all_items()
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     test_stored_procedure_call_search_category()
    # except Exception as e:
    #     print(e)
    #
    # test_repr_vs_str()
    #
    # test_strong_typing()
    #
    # test_import()

    test_parameter_to_kwarg()

    test_enum_creation()

    test_return_values()

    test_enumerate_dict()


    print('End')
