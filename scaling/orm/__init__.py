# -*- coding: utf-8 -*-
# _toolbox operation
__author__ = 'wan'
import pymongo
import os
import re
from ConfigParser import ConfigParser


class DBUtils():
    def __init__(self):
        pass

    @staticmethod
    def read_config():
        db = ConfigParser()
        db.read(os.path.join(os.path.pardir, 'conf/dbconfig.cfg'))
        db_access = DBAccess()
        for option in db.options('db'):
            setattr(db_access, option, db.get('db', option))
        return db_access


class DBAccess():
    def __init__(self):
        pass


class DefaultConditionUtil():
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args

    def get_limit(self):
        if 'limit' in self.kwargs:
            return self.kwargs['limit']
        return 20

    def get_offset(self):
        if 'offset' in self.kwargs:
            return self.kwargs['offset']
        return 1

    def sort_style(self):
        if 'desc_field' in self.kwargs:
            return [(self.kwargs['desc_field'], pymongo.DESCENDING)]
        if 'inc_field' in self.kwargs:
            return [(self.kwargs['inc_field'], pymongo.DESCENDING)]
        # default sort by _id
        return [('_id', pymongo.DESCENDING)]

    def get_complex_expression(self):
        """
        like datetime,io,memory and son on
        :return:
        """
        # if self.args is not empty
        conditions = {}
        if self.args is not None:
            generator = arr_generator(*self.args)
            for val in self.args:
                if not check_value(val):
                    continue
                conditions.update(**generator.next())
        if self.kwargs is None:
            return conditions
        generator = create_generator(**self.kwargs)
        for key, val in self.kwargs.items():
            if not check_value(val):
                continue
            conditions.update(**generator.next())
        return conditions

    def select_one_expression(self):
        generator = create_generator(**self.kwargs)
        return generator


def create_generator(**kwargs):
    for key, val in kwargs.items():
        if not check_value(val):
            continue
        yield get_expression(key=key, val=val)


def arr_generator(*args):
    for val in args:
        if not check_value(val):
            continue
        yield get_expression(val=val)


# get the char and val
def get_expression(key=None, val=None):
    m = re.search("(?<=)[^\w]+", val)
    char = m.group(0)
    e_key, e_val = val.split(char)
    if key is None:
        key = e_key
    # if expression is xx>dd
    return eval('Field("{0}"){1}"{2}"'.format(key, char, e_val))


def check_value(val):
    val = str(val)
    return '>' in val or '<' in val or '=' in val


class Field(object):
    def __init__(self, field):
        self.field = field

    def __lt__(self, value):
        return {self.field: {"$lt": value}}

    def __le__(self, value):
        return {self.field: {"$lte": value}}

    def __ge__(self, value):
        return {self.field: {"$gte": value}}

    def __eq__(self, value):
        return {self.field: value}

    def __ne__(self, value):
        return {self.field: {"$ne": value}}

    def __gt__(self, value):
        return {self.field: {"$gt": value}}

    def inline(self, *value):
        return {self.field: {"$in": value}}

    def not_in(self, *value):
        return {self.field: {"$nin": value}}

    def all(self, *value):
        return {self.field: {"$all": value}}

    def size(self, *value):
        return {self.field: {"$size": value}}

    def type(self, value):
        if type(value) is int and 1 <= value <= 255:
            return {self.field: {"$type": value}}
        if type(value) is str:
            value = value.strip().lower()
            code = 2  # 默认为字符串类型
            # 数字类型
            if value in ("int", "integer", "long", "float", "double", "short", "byte", "number"):
                code = 1
            # 字符串类型
            elif value in ("str", "string", "unicode"):
                code = 2
            # object 类型
            elif value == "object":
                code = 3
            # array 类型
            elif value in ("array", "list", "tuple"):
                code = 4
            # binary data 类型
            elif value in ("binary data", "binary"):
                code = 5
            # object id 类型
            elif value in ("object id", "id"):
                code = 7
            # boolean 类型
            elif value in ("boolean", "bool"):
                code = 8
            # date 类型
            elif value == "date":
                code = 9
            # null 类型
            elif value in ("null", "none"):
                code = 10
            # regular expression 类型
            elif value in ("regular expression", "regular"):
                code = 11
            # javascript code 类型
            elif value in ("javascript code", "javascript", "script"):
                code = 13
            # symbol 类型
            elif value == "symbol":
                code = 14
            # javascript code with scope 类型
            elif value == "javascript code with scope":
                code = 15
            # 32-bit integer 类型
            elif value in ("32-bit integer", "32-bit"):
                code = 16
            # timestamp 类型
            elif value in ("timestamp", "time"):
                code = 17
            # 64-bit integer 类型
            elif value in ("64-bit integer", "64-bit"):
                code = 18
            # min key 类型
            elif value == "min key":
                code = 255
            # max key 类型
            elif value == "max key":
                code = 127
            return {self.field: {"$type": code}}
