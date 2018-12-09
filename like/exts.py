# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_login import LoginManager

db = SQLAlchemy()
bs = Bootstrap()
csrf = CSRFProtect()
moment = Moment()
login = LoginManager()


@login.user_loader
def load_user(user_id):
    from like.models import User
    user = User.query.get(int(user_id))
    return user

login.login_view = 'auth.login'
