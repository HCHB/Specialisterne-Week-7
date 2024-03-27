import functools


def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


def print_decorator(arg1):
    def add_function(function):
        @functools.wraps(function)
        def decorator(*args, **kwargs):
            print()
            print(f'--------------------------')
            print(f'{name}:')
            return_values = function(*args, **kwargs)
            print(f'--------------------------')
            print()
            return return_values
        return decorator

    if type(arg1) is str:
        name = arg1
        return add_function
    else:
        name = arg1.__name__
        return add_function(arg1)
