"""
Application Model
"""
from config import APP_NAME
from flask import Flask
from model import mysql


def register_connection_pool(app: Flask):
    app.db = mysql.get_conn()
    pass


def init_db(config=None):
    """Model Init Function"""

    # MongoDB Init
    initializer = mysql.ModelInitializer()
    initializer.init_model()
    print("[%s] MySQL DATABASE Initialization Completed." % APP_NAME)