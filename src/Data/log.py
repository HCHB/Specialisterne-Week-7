import datetime


class Log:
    _id: int
    _event_name: str
    _table_name: str
    _user_name: str
    _date: type(datetime)

    _data_fields = []  # TODO should this even exists?

    def __init__(self, log_id, event_name, table_name, user_name, event_date):
        self._id = log_id
        self._event_name = event_name
        self._table_name = table_name
        self._user_name = user_name
        self._date = event_date

    def add(self):  # TODO should this even be possible? or raise an exception?
        return False

    def update(self, parameters=None):  # TODO should this even be possible? or raise an exception?
        return False

    def remove(self):  # TODO should this even be possible? or raise an exception?
        return False

    @classmethod
    def get_fields(cls):
        return cls._data_fields

    def __str__(self):
        return (f'ID: {self._id}, '
                f'Event: {self._event_name}, '
                f'Table: {self._table_name}, '
                f'Username: {self._user_name}, '
                f'Event time: {self._date}')
