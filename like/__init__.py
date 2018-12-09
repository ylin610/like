# coding:utf-8
from flask import Flask
from like.exts import db, bs, csrf, moment
import os
from like.settings import config
from like.models import Permission, Role, User, Post, Discussion, Topic
from like.blueprints import front_bp, api_bp
from like.fakes import *
import click


def create_app(config_type=None):
    if config_type is None:
        config_type = os.getenv('FLASK_ENV', 'production')

    app = Flask('like')
    app.config.from_object(config[config_type])

    register_blueprints(app)
    register_exts(app)
    register_shell_context(app)
    register_commands(app)

    return app


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(api_bp)


def register_exts(app):
    db.init_app(app)
    bs.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,
                    Permission=Permission,
                    Role=Role,
                    User=User,
                    Discussion=Discussion,
                    Topic=Topic,
                    Post=Post)


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
        fake_topics()
        fake_posts()
        fake_comments()
        fake_discussion()
        click.echo('虚拟数据生成完毕！')
