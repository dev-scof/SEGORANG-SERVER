from abc import ABCMeta, abstractmethod
from datetime import datetime
import MySQLdb
from config import config


class Model(metaclass=ABCMeta):

    VERSION = 1

    def __init__(self, cursor) -> None:
        self.table_name = self.__class__.__name__.lower()
        self.cursor = cursor
    
    @property
    def schema(self) -> dict:
        """Get default document format"""
        return {
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def create_index(self) -> None:
        pass

    def create_table(self) -> None:
        """Create Table"""
        sql = open(f"model/mysql/sqls/tables/{self.table_name}.sql").read()
        self.cursor.execute(sql)