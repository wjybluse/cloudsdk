# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from scaling.orm import DefaultConditionUtil


class TestComplexConditions(unittest.TestCase):
    def test_create_complex(self):
        dct = DefaultConditionUtil(cpu='u<=1000', ram='>=100000', mysql='>=50000', redis='<121312321', tomcat='>432432')
        self.assertIsNotNone(dct.get_complex_expression())
        print(dct.get_complex_expression())

    def test_all_method(self):
        dct = DefaultConditionUtil(cpu='<=1000', ram='>=100000', mysql='>=50000', redis='<121312321', tomcat='>432432',
                                   limit=20, offset=10, desc_field='name', inc_field='age')
        self.assertEqual(
            {'ram': {'$gte': 100000}, 'redis': {'$lt': 121312321}, 'cpu': {'$lte': 1000}, 'tomcat': {'$gt': 432432},
             'mysql': {'$gte': 50000}},
            dct.get_complex_expression())
        self.assertEqual(dct.get_limit(), 20)
        self.assertEqual(dct.get_offset(), 10)
        self.assertIsNotNone(dct.sort_style())

    def test_create_condition(self):
        hash = dict(name='wan', age='>10', cpu='>100', disk='>5000', info='private', desc_field='name')
        dct = DefaultConditionUtil(**hash)
        print(dct.get_complex_expression())
        self.assertIsNotNone(dct.get_complex_expression())
