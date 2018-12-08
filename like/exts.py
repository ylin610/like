# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect

db = SQLAlchemy()
bs = Bootstrap()
csrf = CSRFProtect()
