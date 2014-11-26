# -*- coding: utf-8 -*-
__author__ = 'wan'


class RequestError(Exception):
    def __init__(self, code, msg):
        self.message = msg
        self.code = code
        Exception.__init__(self)


class Test():
    def __init__(self, ):
        self.ret = None

    def number(self, name=None):
        self.ret = int(name)
        return self.ret


if __name__ == '__main__':
    test = Test()
    print(test.number(name='dsadsa'))