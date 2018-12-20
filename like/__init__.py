# coding:utf-8
from flask import Flask
from like.exts import db, csrf, moment, login, mail, socketio, whooshee, migrate
import os
from like.settings import config
from like.models import Permission, Role, User, Post, Discussion, Topic, Comment
from like.blueprints import front_bp, api_bp, auth_bp, user_bp, disc_bp
from like.fakes import *
import click
from like.utils import Mongo
from flask_login import current_user
import logging
from logging.handlers import RotatingFileHandler


def create_app(config_type=None):
    if config_type is None:
        config_type = os.getenv('FLASK_ENV', 'production')

    app = Flask('like')
    app.config.from_object(config[config_type])

    register_logger(app)
    register_blueprints(app)
    register_exts(app)
    register_shell_context(app)
    register_commands(app)
    register_app_context(app)

    return app


def register_logger(app):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s: %(message)s')
    handler = RotatingFileHandler('logs/like.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(handler)


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(disc_bp)


def register_exts(app):
    db.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    whooshee.init_app(app)
    migrate.init_app(app, db)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,
                    Permission=Permission,
                    Role=Role,
                    User=User,
                    Discussion=Discussion,
                    Topic=Topic,
                    Post=Post,
                    Comment=Comment)


def register_app_context(app):
    @app.context_processor
    def make_app_template_context():
        if current_user.is_authenticated:
            count = Mongo.count({'user_id': current_user.id, 'is_read': False})
            return {'unread_count': count}
        return {}


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除已存在的表')
    def init_db(drop):
        """初始化数据库"""
        if drop:
            click.confirm('确认要删除所有数据表吗？', abort=True)
            db.drop_all()
            click.echo('已删除所有数据表。')
        click.echo('初始化数据库……')
        db.create_all()
        click.echo('数据库初始化完毕。')
        click.echo('初始化管理员……')
        click.echo('管理员初始化完毕。')

    @app.cli.command()
    def forge():
        """初始化数据库，并生成虚拟数据"""
        click.echo('正在初始化数据库...')
        db.drop_all()
        db.create_all()
        Permission.init_permission()
        Role.init_role()
        click.echo('数据库初始化完毕！\n正在生成虚拟数据...')
        fake_users()
        fake_follows()
        fake_topics()
        fake_posts()
        fake_comments()
        fake_discussion()
        click.echo('虚拟数据生成完毕！')
