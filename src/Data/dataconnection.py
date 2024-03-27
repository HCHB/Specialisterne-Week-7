import mysql.connector

from src.decorators import singleton


@singleton
class DataConnection:
    _database_name: str
    _user: str
    _password: str

    def __init__(self, database_name):
        self._database_name = database_name

    def authenticate(self, username, password):
        try:
            with (mysql.connector.connect(user=username,
                                          password=password,
                                          host='localhost',
                                          database='hebo_week_7')):
                self._user = username
                self._password = password
                return True
        except mysql.connector.errors.ProgrammingError as e:
            return False

    def logout(self):
        self._user = ''
        self._password = ''
        return True

    def execute_procedure(self, command, values):
        with (mysql.connector.connect(user=self._user,
                                      password=self._password,
                                      host='localhost',
                                      database='hebo_week_7') as connection):

            with connection.cursor(dictionary=True) as cursor:
                cursor.callproc(procname=command, args=values)
                stored = cursor.stored_results()
                result_sets = [r.fetchall() for r in stored]

                connection.commit()

                if len(result_sets) == 1 and len(result_sets[0]) == 1 and len(result_sets[0][0]) == 1:
                    return next(iter(result_sets[0][0]))
                elif len(result_sets) == 1 and len(result_sets[0]) == 1:
                    return result_sets[0][0]
                elif len(result_sets) == 1:
                    return result_sets[0]
                else:
                    return result_sets

    def execute_command(self, command, values):
        with (mysql.connector.connect(user=self._user,
                                      password=self._password,
                                      host='localhost',
                                      database='hebo_week_7') as connection):
            with connection.cursor(prepared=True, dictionary=True) as cursor:
                cursor.execute(command, values)
                results = cursor.fetchall()

                connection.commit()

                return results
