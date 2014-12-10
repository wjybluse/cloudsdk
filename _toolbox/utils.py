# -*- coding: utf-8 -*-
__author__ = 'wan'
import urllib
import sys

"""
can not find
"""
ENCODING = 'utf-8'


def encode(s):
    s = str(s)
    res = urllib.quote(s.decode(sys.stdin.encoding).encode(ENCODING), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


class Utils():
    def __init__(self):
        pass

    @staticmethod
    def close(obj):
        try:
            getattr(obj, 'close')()
        except AttributeError:
            pass

    @staticmethod
    def kill(obj):
        try:
            getattr(obj, 'kill')()
        except AttributeError:
            pass

    @staticmethod
    def is_empty(params):
        if params is None:
            return True
        if isinstance(params, dict) or isinstance(params, list) or isinstance(params, str):
            if len(params) <= 0:
                return True
        return False

    @staticmethod
    def contains(params, key):
        if params is None:
            return False
        if isinstance(params, str):
            return key in params
        if isinstance(params, dict) or isinstance(params, list):
            return params.__contains__(key)
        return False

    @staticmethod
    def is_expression(string):
        return '>' in string or '<' in string or '=' in string


class RouteError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__


class RestError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__


class ScaleError(Exception):
    ACTION_NOT_SUPPORT = 0x0001
    PARAMS_INVALID = 0x0002

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__