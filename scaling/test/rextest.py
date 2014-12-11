# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
import re
from scaling.orm import Field


class TestRex(unittest.TestCase):
    def setUp(self):
        self.re = lambda ss: re.search("(?<=)[^\w]+", ss)

    def test_find_val(self):
        s = '<=nihao'
        m = self.re(s)
        ret = m.group(0)
        self.assertIsNotNone(ret)
        self.assertEqual('<=', ret)

    def test_single_char(self):
        s = '>=nihao'
        m = re.search("(?<=)[^\w]+", s)
        ret = m.group(0)
        self.assertIsNotNone(ret)
        self.assertEqual('>=', ret)

    def test_eval_value(self):
        ss = 'dadsa'
        s = 'Field("' + ss + '"){0}{1}'.format('>=', 5)
        expression = eval(s)
        print(expression)
        self.assertIsNotNone(expression)
        self.assertEqual(Field('dadsa') >= 5, expression)

    def test_two_value(self):
        ss = 'usage>90%'
        m = self.re(ss)
        print(m.group(0))
        arr = ss.split(m.group(0))
        print(arr)
        self.assertIsNotNone(m.group(0))

    def test_tuple(self):
        dl = ['nihao', 'dasdasds', 'dasdsadsadas']
        dd = TTTT(*dl)
        dd._print()


class TTTT():
    def __init__(self, *arg):
        self.arg = arg

    def _print(self):
        for r in self.arg:
            print(r)


if __name__ == '__main__':
    unittest.main()