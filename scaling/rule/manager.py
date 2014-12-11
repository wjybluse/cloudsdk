# -*- coding: utf-8 -*-
__author__ = 'wan'
from scaling.orm.mongo import DBServer
from cloudsdk.tool.logger import LogFactory

logger = LogFactory.logger(__file__)


class RuleManager():
    def __init__(self):
        """
        db client DBServer('collection','table')
        """
        self.db = DBServer('rule', 'tasks')

    def register(self, rule, **condition):
        """
        :param rule: unique name
        :param condition:
        :return:
        """
        if self.db.find_one(**{'_name': rule}):
            logger.error("The rule name is exist.", "Rule name=", rule)
            raise ValueError("Duplicate key error")
        self.db.insert(condition)

    def deregister(self, rule):
        """
        :param rule: rule name
        :return:
        """
        self.db.delete(pattern={'_name': rule})

    def list_rules(self):
        return self.db.find_all()

    def query(self, **condition):
        return self.db.query(**condition)

    def close(self):
        self.db.close()

    def __del__(self):
        self.db.close()