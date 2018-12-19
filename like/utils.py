# coding: utf-8
from flask import jsonify
import string
import random


def generate_captcha(num=6, use_letter=False):
    """Generate captcha with numbers and optional letters.

    :param num : Length of the captcha.
    :param use_letter : Generate captcha with both numbers and letters or not.
    :return : The generated captcha.
    """
    sample = string.digits
    if use_letter:
        sample += string.ascii_letters
    return ''.join(random.sample(sample, num))


def get_max(q, num=1, key=None):
    """Get a number of max items from an iterable.

    :param q : The sample.
    :param num : The number of items to get.
    :param key : A specific function to order the iterable.
    :return : A result item when param num is 1,
        or a list of result items. Return None if q is empty.
    """
    if len(q) == 0:
        return None
    elif num == 1:
        return max(q, key=key)
    else:
        return sorted(q, key=key)[0:num]


class Restful:
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500

    @classmethod
    def success(cls, message='成功', data=None):
        return jsonify({'code': cls.ok, 'message': message, 'data': data})

    @classmethod
    def unauth_error(cls, message='没有权限', data=None):
        return jsonify({'code': cls.unautherror, 'message': message, 'data': data})

    @classmethod
    def params_error(cls, message='参数错误', data=None):
        return jsonify({'code': cls.paramserror, 'message': message, 'data': data})

    @classmethod
    def server_error(cls, message='服务器内部错误', data=None):
        return jsonify({'code': cls.servererror, 'message': message, 'data': data})


class Memcached:
    import memcache
    cache = memcache.Client(['127.0.0.1:11211'], debug=True)

    @classmethod
    def set(cls, key, value, timeout=60):
        return cls.cache.set(key, value, timeout)

    @classmethod
    def get(cls, key):
        return cls.cache.get(key)

    @classmethod
    def delete(cls, key):
        return cls.cache.delete(key)


class Mongo:
    import pymongo
    client = pymongo.MongoClient()
    coll = client.my_app.notifications

    @classmethod
    def insert_one(cls, *args, **kwargs):
        return cls.coll.insert_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return cls.coll.update_many(*args, **kwargs)

    @classmethod
    def aggregate(cls, *args, **kwargs):
        return cls.coll.aggregate(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return cls.coll.count_documents(*args, **kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.coll.find(*args, **kwargs)
