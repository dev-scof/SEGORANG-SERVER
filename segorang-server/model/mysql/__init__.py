from config import config
import MySQLdb
from .user import User
from .board import Board
MODELS = [
    User, Board
]

def get_connection(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_NAME
    ):

    return MySQLdb.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            use_unicode=True,
            database=db,
            charset="utf8"
        )


class ModelInitializer:
    """TEST"""
    def __init__(self) -> None:
        self.host=config.MYSQL_HOST
        self.port=config.MYSQL_PORT
        self.user=config.MYSQL_USER
        self.password=config.MYSQL_PASSWORD
        self.db=config.MYSQL_NAME
    
    @property
    def cursor(self):
        return get_connection(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db
        )
    
    def init_model(self):
        """Initializer All Process"""
        with self.cursor as cur:
            self.init_tables(cur)

    @staticmethod
    def init_tables(cur):
        """Create Table each Tables"""
        for model in MODELS:
            model(cur).create_table()