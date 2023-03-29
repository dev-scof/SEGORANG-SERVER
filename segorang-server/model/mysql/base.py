from abc import ABCMeta, abstractmethod
from datetime import datetime
from config import config
from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor

class Model(metaclass=ABCMeta):

    VERSION = 1

    def __init__(self, conn) -> None:
        self.table_name = self.__class__.__name__.lower()
        self.conn:Connection = conn
        self.cursor:Cursor = conn.cursor()

    @property
    def insert_query(self) -> str:
        """Get Default insert query format"""
        return "INSERT INTO {table_name}({keys}) VALUES({values});"

    @property
    def select_query(self) -> str:
        """Get Default select query format"""
        return "SELECT {property} FROM {table_name} {condition};"

    @property
    def delete_query(self) -> str:
        """Get Default delete query format"""
        return "DELETE FROM {table_name} {condition};"

    @property
    def update_query(self) -> str:
        """Get Default update query format"""
        return "UPDATE {table_name} SET {update_data} {condition}"

    def create_index(self) -> None:
        pass

    def create_table(self) -> None:
        """Create Table"""
        sql = open(f"model/mysql/sqls/tables/{self.table_name}.sql").read()
        self.cursor.execute(sql)