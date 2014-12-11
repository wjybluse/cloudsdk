# -*- coding: utf-8 -*-
# db operation
# provider curd method
__author__ = 'wan'
from pymongo.mongo_client import MongoClient

from _toolbox.logger import LogFactory
from _toolbox.logger import log
from . import DBUtils
from . import DefaultConditionUtil


logger = LogFactory.logger(__file__)


class DBServer():
    def __init__(self, collection_name, table):
        self.collection_name = collection_name
        self.table = table
        cfg = DBUtils.read_config()
        url = "mongodb://{0}:{1}/".format(cfg.host, cfg.port)
        logger.debug("The db url", url)
        self._client = MongoClient(url)
        # can not connect to any db except admin server
        username, password = getattr(cfg, 'username', ''), getattr(cfg, 'password', '')
        if not (len(username) <= 0 or len(password) <= 0):
            self._client.admin.authenticate(cfg.username, cfg.password)
        db = self._client[collection_name]
        self.table = db[table]

    @log
    def query(self, pattern=None, **condition):
        """
        :param pattern: dict pattern suitable
        :param condition: condition to pagination
        :return:suitable information
        """
        if pattern is None:
            # if pattern is None,the conditions must be empty
            values = self.table.find().limit(20)
            return convert_list(values)
        if condition is None or len(condition) <= 0:
            # if condition is empty
            values = self.table.find(pattern)
            return convert_list(values)
        dcu = DefaultConditionUtil(**condition)
        if dcu.get_complex_expression() is not None:
            pattern = pattern.update(**dcu.get_complex_expression())
        ret = self.table.find(pattern).skip(dcu.get_offset()).limit(dcu.get_limit()).sort(dcu.sort_style())
        return convert_list(ret)

    @log
    def find_one(self, **condition):
        one = self.table.find_one(condition)
        return convert_dict(one)

    @log
    def find_all(self):
        """
        :return: all information
        """
        values = self.table.find()
        return convert_list(values)

    @log
    def insert(self, obj):
        self.table.insert(obj)

    @log
    def delete(self, pattern=None, **condition):
        """
        :param id: remove obj id
        :param pattern: pattern data
        :param condition:suitable data
        :return:nothing
        """
        if pattern is None:
            return
        self.table.remove(pattern)

    @log
    def update(self, pattern=None, **new):
        """
        :param id: update id
        :param other: condition
        :param new: new data
        :return:
        """
        self.table.update(pattern, new)

    @log
    def query_by_complex_condition(self, code):
        """
        :param code: query information via complex condition use javascript code
        :return:
        """
        values = self.table.find().where(code)
        return convert_list(values)

    @log
    def count(self, id=None, **conditions):
        if id is None and conditions is None:
            return {'count': self.table.find().count()}
        if conditions is None:
            return {'count': self.table.find(dict(id=id)).count()}
        if id is None:
            return {'count': self.table.find(conditions).count()}
        conditions['id'] = id
        return {'count': self.table.find(conditions)}

    @log
    def close(self):
        self._client.close()

    def __del__(self):
        self._client.close()


def convert_list(data):
    ret = []
    for item in data:
        if isinstance(item, list):
            ret.append(convert_list(item))
        elif isinstance(item, dict):
            ret.append(convert_dict(item))
        else:
            ret.append(str(item))
    return ret


def convert_dict(data):
    if data is None:
        return None
    value = {}
    for k, v in data.items():
        if isinstance(v, list):
            value[str(k)] = convert_list(v)
        elif isinstance(v, dict):
            value[str(k)] = convert_dict(v)
        else:
            value[str(k)] = str(v)
    return value
