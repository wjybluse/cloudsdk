# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from scaling.orm import Field


class FieldTest(unittest.TestCase):
    def test_gt_ok(self):
        f = Field('hha')
        ret = f > 10
        self.assertIsNot(ret, True)
        self.assertIsNot(ret, False)
        self.assertIsInstance(ret, dict)
        print(ret)

    def test_lt_ok(self):
        f = Field('hha')
        ret = f < 10
        self.assertIsNot(ret, True)
        self.assertIsNot(ret, False)
        self.assertIsInstance(ret, dict)
        print(ret)