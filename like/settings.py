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

    POSTS_PER_PAGE = 20


class DevelpomentConfig(BaseConfig):
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
