# coding:utf-8
from flask import Flask
from like.exts import db
import os
from like.settings import config
from like.models import Permission, Role, User


def create_app(config_type=None):
    if config_type is None:
        config_type = os.getenv('FLASK_ENV', 'production')

    app = Flask('like')
    app.config.from_object(config[config_type])

    register_exts(app)
    register_shell_context(app)
    register_commands(app)

    return app


def register_exts(app):
    db.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Permission=Permission, Role=Role, User=User)


def register_commands(app):
    @app.cli.command()
    def init_db():
        """Initial database"""
        db.create_all()
