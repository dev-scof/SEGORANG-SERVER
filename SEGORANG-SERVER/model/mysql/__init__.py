from pymysql import connect
from config import config
from flask import g
# Tables


MODELS = [
    # Here is tables
]


def get_db(
    host: str = config.MYSQL_HOST,
    port: int = config.MYSQL_PORT,
    user: str = config.MYSQL_USER,
    password: str = config.MYSQL_PASSWORD,
    db: str = config.MYSQL_DB,
    charset: str = "utf8"
) -> connect:
    db = connect(
        host=host,
        port=port,
        user=user,
        passwd=password,
        db=db,
        charset=charset
    )
    return db


class ModelInitializer:
    def __init__(self) -> None:
        self.host = config.MYSQL_HOST
        self.port = config.MYSQL_PORT
        self.user = config.MYSQL_USER
        self.passwd = config.MYSQL_PASSWORD
        self.db = config.MYSQL_DB
        self.charset = "utf8"

    @property
    def db(self):
        """ property of database"""
        return get_db()

    @staticmethod
    def init_db():
        """
        Initialize Databases 
        execute sql queries
            - create tables
            - create records
        """
        if 'db' not in g:
            g.db = get_db()
        with g.db.cursor() as cur:
            pass
        g.db.commit()
        g.db.close()
