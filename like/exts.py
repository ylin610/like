# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_moment import Moment

db = SQLAlchemy()
bs = Bootstrap()
csrf = CSRFProtect()
moment = Moment()
