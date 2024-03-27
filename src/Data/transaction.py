import datetime

from src.project_enums import TransactionTypes

from src.Data.dataconnection import DataConnection


class Transaction:
    _id: str
    _item_id: str
    _transaction_time: type(datetime)
    _amount: int
    _type: type(TransactionTypes)

    _data_fields = ['item_id', 'amount', 'transaction_type']

    def __init__(self, item_id, amount, transaction_type, transaction_id=None, transaction_time=None):
        self._type = TransactionTypes(transaction_type)
        self._amount = amount
        self._transaction_time = transaction_time
        self._item_id = item_id
        self._id = transaction_id

    def add(self):
        command = 'add_transaction'
        values = [self._item_id, self._amount, self._type.value]

        connection = DataConnection()
        values = connection.execute_procedure(command, values)

        self._transaction_time = values['transaction_time']
        self._id = values['transaction_id']

    def update(self, parameters=None):  # TODO should this even be possible? or raise an exception?
        return False

    def remove(self):  # TODO should this even be possible? or raise an exception?
        return False

    @classmethod
    def get_fields(cls):
        return cls._data_fields

    def __str__(self):
        return (f'ID: {self._id}, '
                f'Item ID: {self._item_id}, '
                f'Transaction type: {self._type.value}, '
                f'Amount: {self._amount}, '
                f'Transaction time: {self._transaction_time}')
