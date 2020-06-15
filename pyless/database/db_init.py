import peewee as pw
from pyless.database.models import *
from pyless.database.dao.child_daos.loans_dao import LoansDao


class DbInit:
    __db = None

    def __init__(self, credentials):
        # We get it from context for add user, where its not an API call, for api calls get it from the env variable
        self.__db = self.init_db_connection(credentials)
        proxy.initialize(self.__db)
        self.loans = LoansDao(self.__db)

    @staticmethod
    def init_db_connection(credentials):
        print("Attempting to connect to DB")
        try:
            db = pw.PostgresqlDatabase(credentials['dbName'],
                                       host=credentials['host'],
                                       port=credentials['port'],
                                       user=credentials['username'],
                                       password=credentials['password'])
                                       #connect_timeout=2)
            print("Connected to DB successfully")
            return db
        except Exception as e:
            raise e

    def get_connection(self):
        return self.__db

    def close_connection(self):
        print(type(self.__db))
        try:
            proxy.close()
            print("CLOSED")
        except Exception as e:
            print(e)
