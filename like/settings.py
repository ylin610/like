# coding: utf-8
import os


root_path = os.path.dirname(os.path.abspath('.'))
if os.name == 'nt':
    sqlite3 = 'sqlite:///'
else:
    sqlite3 = 'sqlite:////'


class BaseConfig:
    # basic config
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelpomentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = sqlite3 + os.path.join(root_path, 'data_dev.db')