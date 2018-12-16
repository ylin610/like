# coding: utf-8
from flask import jsonify
import string
import random


def generate_captcha(num=6, use_letter=False):
    """generate captcha with numbers and optional letters.

    :param num (int): length of the captcha.
    :param use_letter (bool): generate captcha with both numbers and letters or not.
    :return (str): returns the generated captcha.
    """
    sample = string.digits
    if use_letter:
        sample += string.ascii_letters
    return ''.join(random.sample(sample, num))


def get_max(q, num=1, key=None):
    """get a number of max items from an iterable.

    :param q (iterable): the sample.
    :param num (int): the number of items to get.
    :param key (function): a specific function to order the iterable.
    :return (obj or list or None): a result item when param num is 1,
        or a list of result items. Return None if q is empty.
    """
    if len(q) == 0:
        return None
    elif num == 1:
        return max(q, key=key)
    else:
        return sorted(q, key=key)[0:num]


class Restful(object):
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


class Memcached(object):
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


class Redis():
    import redis
    cache = redis.Redis()

    @classmethod
    def incr(cls, disc):
        return cls.cache.incr(disc)

    @classmethod
    def decr(cls, disc):
        return cls.cache.decr(disc)
