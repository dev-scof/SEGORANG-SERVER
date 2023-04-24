from config import config
import MySQLdb
from .user import User
from .board import Board
from .post import Post
from .bookmark import Bookmark
from .comment import Comment
from .comment_like import Comment_Like
from .comment_report import Comment_Report
from .post_image import Post_Image
from .post_like import Post_Like
from .post_report import Post_Report
from .user_image import User_Image
from .youtube import Youtube
MODELS = [
    User, User_Image, Board, Post, Bookmark, 
    Comment, Comment_Like, Comment_Report,
    Post_Image, Post_Report, Post_Like, Youtube
]

def get_conn(
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
            db=db,
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
        return get_conn(
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
        # Remove FK Check
        cur.cursor().execute('SET foreign_key_checks = 0;')
        # create tables
        for model in MODELS:
            model(cur).create_table()
        # add constrain
        sql = open(f"model/mysql/sqls/tables/add_constrain.sql").read()
        cur.cursor().execute(sql)
        # FK Check
        cur.cursor().execute('SET foreign_key_checks = 1;')