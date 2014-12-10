# -*- coding: utf-8 -*-
__author__ = 'wan'


class RequestError(Exception):
    def __init__(self, code, msg):
        self.message = msg
        self.code = code
        Exception.__init__(self)
