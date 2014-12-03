# -*- coding: utf-8 -*-
__author__ = 'wan'
SCALE_TYPE = ['REDIS', 'SERVER', 'MYSQL']


class ScaleType():
    def __init__(self):
        add_properties(self)


def add_properties(obj):
    for property in SCALE_TYPE:
        setattr(obj, property.lower(), property)
