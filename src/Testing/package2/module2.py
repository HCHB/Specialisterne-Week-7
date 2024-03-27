from src.Testing.package.module import ClassName
from src.decorators import singleton


@singleton
class ClassName2:
    def import_print(self):
        print('inside 2')
        test = ClassName()
        test.import_print()