# coding: utf-8
import os


root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if os.name == 'nt':
    sqlite3 = 'sqlite:///'
else:
    sqlite3 = 'sqlite:////'


class BaseConfig:
    # basic config
    SECRET_KEY = os.getenv('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True

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

    POSTS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 8


class DevelpomentConfig(BaseConfig):
    database_type = os.getenv('DATABASE_TYPE')
    if database_type == 'mysql':
        HOSTNAME = '127.0.0.1'
        PORT = '3306'
        DATABASE = 'test'
        USERNAME = os.getenv('MYSQL_USERNAME')
        PASSWORD = os.getenv('MYSQL_PASSWORD')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
    else:
        SQLALCHEMY_DATABASE_URI = sqlite3 + os.path.join(root_path, 'data_dev.db')


class ProductionConfig(BaseConfig):
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
