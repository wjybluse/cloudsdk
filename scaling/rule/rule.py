# -*- coding: utf-8 -*-
__author__ = 'wan'
from scaling.orm.mongo import DBServer


class Rule():
    cls = None

    def __init__(self):
        self.server = DBServer('rule', 'tasks')


    def _find(self, pattern=None, **conditions):
        return self.server.query(pattern=pattern, **conditions)

    def _find_all(self):
        return self.server.find_all()

    @staticmethod
    def validate(key, condition):
        server = DBServer(key, 'tasks')
        # should add datetime support?
        ret = server.query(pattern=condition)
        server.close()
        if ret is None or len(ret) <= 0:
            return False
        return True

    # send alarm
    @staticmethod
    def send_alarm(data):
        server = DBServer('alarm', 'tasks')
        server.insert(data)
        server.close()

    @classmethod
    def find(cls, pattern=None, **conditions):
        return cls.instance()._find(pattern=pattern, **conditions)

    @classmethod
    def find_all(cls):
        return cls.instance()._find_all()

    @classmethod
    def instance(cls):
        if cls.cls is None:
            cls.cls = cls()
        return cls.cls
