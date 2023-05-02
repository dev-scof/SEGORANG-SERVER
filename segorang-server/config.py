'''
Application Config Setting
'''
import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))
APP_NAME = "SEGORANG"
FLASK_CONFIG = os.getenv('FLASK_CONFIG') or 'development'
# ENV 관리
ENV_FILE = f'{FLASK_CONFIG}.env'
ENV_PATH = os.path.join(ROOTDIR, 'requirements')
load_dotenv(dotenv_path=os.path.join(ENV_PATH, ENV_FILE), verbose=True)

class Config:
    '''General Config'''
    SLOW_API_TIME = 0.5
    API_LOGGING = False
    JSON_AS_ASCII = False
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 24 * 365
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 24 * 365
    JWT_SESSION_COOKIE = False
    SECRET_KEY = os.environ[APP_NAME + "_SECRET_KEY"]

    # MySQL
    MYSQL_HOST = os.environ[APP_NAME + "_MYSQL_HOST"]
    MYSQL_PORT = os.environ[APP_NAME + "_MYSQL_PORT"]
    MYSQL_USER = os.environ[APP_NAME + "_MYSQL_USER"]
    MYSQL_PASSWORD = os.environ[APP_NAME + "_MYSQL_PASSWORD"]
    MYSQL_NAME = os.environ[APP_NAME + "_MYSQL_NAME"]
    

    # S3
    S3_DOMAIN = os.environ[APP_NAME + "_S3_DOMAIN"]
    S3_BUCKET_NAME = os.environ[APP_NAME + "_S3_BUCKET_NAME"]
    S3_ACCESS_KEY_ID = os.environ[APP_NAME + "_S3_ACCESS_KEY_ID"]
    S3_SECRET_ACCESS_KEY = os.environ[APP_NAME + "_S3_SECRET_ACCESS_KEY"]
    S3_BUCKET_ACL_POLICY = os.environ[APP_NAME + "_S3_BUCKET_ACL_POLICY"]

    # Admin
    ADMIN_ID = os.environ[APP_NAME + '_ADMIN_ID']
    ADMIN_PW = os.environ[APP_NAME + '_ADMIN_PW']


    @staticmethod
    def init_app(app):
        pass


if FLASK_CONFIG == 'development':
    class AppConfig(Config):
        DEBUG = True
        TESTING = False
elif FLASK_CONFIG == 'production':
    class AppConfig(Config):
        DEBUG = False
        TESTING = False
else:
    raise Exception("Flask Config not Selected.")


config = AppConfig


class TestConfig(Config):
        DEBUG = True
        TESTING = True


if __name__ == '__main__':
    pass
