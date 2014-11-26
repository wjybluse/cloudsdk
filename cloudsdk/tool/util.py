# -*- coding: utf-8 -*-
__author__ = 'wan'
import urllib
import sys

ENCODING = 'utf-8'


def encode(s):
    s = str(s)
    res = urllib.quote(s.decode(sys.stdin.encoding).encode(ENCODING), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res