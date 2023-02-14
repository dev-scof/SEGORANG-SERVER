from abc import ABCMeta, abstractmethod
from datetime import datetime
from config import config


class Model(metaclass=ABCMeta):

    VERSION = 1

    def __init__(self, conn) -> None:
        self.table_name = self.__class__.__name__.lower()
        self.conn = conn
        self.cursor = conn.cursor()

    @property
    def insert_query(self) -> str:
        """Get Default insert query format"""
        return "INSERT INTO {table_name}({keys}) VALUES({values});"

    def create_index(self) -> None:
        pass

    def create_table(self) -> None:
        """Create Table"""
        sql = open(f"model/mysql/sqls/tables/{self.table_name}.sql").read()
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()