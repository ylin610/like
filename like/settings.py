# coding: utf-8
import os
from dotenv import load_dotenv

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(root_path, '.env')
load_dotenv(env_path)
if os.name == 'nt':
    sqlite3 = 'sqlite:///'
else:
    sqlite3 = 'sqlite:////'


class BaseConfig:
    # basic config
    SECRET_KEY = os.getenv('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    POSTS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 8
    CDN_DOMAIN = 'http://cdn.stravel.top'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Avatar
    AVARTA_SIZE = 40

    # Celery
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
    CELERY_BROKER_URL = "redis://127.0.0.1:6379"

    # Flask-Mail
    # 邮箱   TLS     SSL
    # QQ    587     465
    # 163   994     465
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # 七牛云
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')
    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')


class DevelpomentConfig(BaseConfig):
    # database_type = os.getenv('DATABASE_TYPE')
    # if database_type == 'MYSQL':
    #     HOSTNAME = '127.0.0.1'
    #     PORT = '3306'
    #     DATABASE = 'test'
    #     USERNAME = os.getenv('MYSQL_USERNAME')
    #     PASSWORD = os.getenv('MYSQL_PASSWORD')
    #     SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    # else:
    SQLALCHEMY_DATABASE_URI = sqlite3 + os.path.join(root_path, 'data_dev.db')


class ProductionConfig(BaseConfig):
    database_type = os.getenv('DATABASE_TYPE')
    if database_type == 'MYSQL':
        HOSTNAME = '127.0.0.1'
        PORT = '3306'
        DATABASE = 'like_app'
        USERNAME = os.getenv('MYSQL_USERNAME')
        PASSWORD = os.getenv('MYSQL_PASSWORD')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', sqlite3 + os.path.join(root_path, 'data.db'))


class TestConfig(BaseConfig):
    TESTING = True,
    WTF_CSRF_ENABLED = False,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelpomentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
