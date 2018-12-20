# coding: utf-8
from flask import Flask
from celery import Celery
from like.exts import mail
from flask_mail import Message
from like.settings import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
mail.init_app(app)


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def send_email(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)
