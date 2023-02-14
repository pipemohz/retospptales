import pyodbc
import os
from app.settings.environment import DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD


class PyODBC:
    @staticmethod
    def standard_connection():
        """
        Create a database connection to Config.DB_NAME database of SQL Server DB_HOST.
        """
        os_name = os.name
        if os_name == 'nt':
            conn_string = f'Driver={{SQL Server}};Server={DB_HOST};Database={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD}'
        else:
            conn_string = f'Driver={{ODBC Driver 17 for SQL Server}};Server={DB_HOST};Database={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD}'

        return pyodbc.connect(conn_string)


class Connection:
    def __init__(self) -> None:
        self.conn = PyODBC.standard_connection()

    def __enter__(self):
        return self.conn

    def __exit__(self, exec_type, exec_value, traceback):
        self.conn.close()
