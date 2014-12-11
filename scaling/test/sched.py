# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from scaling.rule.timerwheel import TimerWheel


class TestWheel(unittest.TestCase):
    def test_wheel_ok(self):
        tw = TimerWheel()
        tw.start()