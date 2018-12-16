# coding: utf-8
from flask import jsonify
import string
import random


def generate_captcha(num=6, use_letter=False):
    """generate captcha with numbers and optional letters.

    :param num : length of the captcha.
    :param use_letter : generate captcha with both numbers and letters or not.
    :return : returns the generated captcha.
    """
    sample = string.digits
    if use_letter:
        sample += string.ascii_letters
    return ''.join(random.sample(sample, num))


def get_max(q, num=1, key=None):
    """get a number of max items from an iterable.

    :param q : the sample.
    :param num : the number of items to get.
    :param key : a specific function to order the iterable.
    :return : a result item when param num is 1,
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
