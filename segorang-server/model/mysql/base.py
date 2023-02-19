from abc import ABCMeta, abstractmethod
from datetime import datetime
from config import config
from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor
from MySQLdb._exceptions import OperationalError
from model.__init__ import register_connection_pool
from flask import current_app
class Model(metaclass=ABCMeta):

    VERSION = 1

    def __init__(self, conn) -> None:
        self.table_name = self.__class__.__name__.lower()
        self.conn:Connection = conn
        self.cursor:Cursor = self.conn.cursor()

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

    def create_index(self) -> None:
        pass

    def create_table(self) -> None:
        """Create Table"""
        sql = open(f"model/mysql/sqls/tables/{self.table_name}.sql").read()
        self.cursor.execute(sql)
    
    # customize cursor_execute
    def execute_by_cursor(self, query):
        try:
            self.cursor.execute(query)
            return True
        except OperationalError as e:
            if e.args[0] == 2006:
                # MySQL server has gone away
                register_connection_pool(current_app)
                self.conn:Connection = current_app.conn
                self.cursor:Cursor = self.conn.cursor()
                self.cursor.execute(query)
                current_app.logger.error(f"MySQL server has gone away error in cursor/ is solved?")
        except Exception as e:
            return e

    # customize connection commit
    def commit_by_conn(self):
        try:
            self.conn.commit()
            return True
        except OperationalError as e:
            if e.args[0] == 2006:
                # MySQL server has gone away
                register_connection_pool(current_app)
                self.conn:Connection = current_app.conn
                self.cursor:Cursor = self.conn.cursor()
                current_app.logger.error(f"MySQL server has gone away error in connection/ is solved?")
        except Exception as e:
            return e

