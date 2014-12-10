# -*- coding: utf-8 -*-
__author__ = 'wan'
from xml.etree import ElementTree as tree

import xmltodict

from _toolbox.logger import LogFactory
from _toolbox.error import RequestError


logger = LogFactory.logger(__name__)


class XmlParser():
    instance = None

    def __init__(self):
        pass

    @staticmethod
    def parser(code, msg):
        if code < 200 or code > 204:
            return _find_error(code, msg)
        return _parser_xml(msg)


def _find_error(status, msg):
    obj = xmltodict.parse(msg)
    obj['status'] = status
    obj['message'] = msg
    logger.error("the error response", obj)
    return obj


def _parser_xml(msg):
    root = tree.fromstring(msg)
    return root


def find_all(doc, name):
    data = []
    prefix = '{%s}' % (doc.tag.split('}')[0].split('{')[1])
    _rec(doc, data, name, prefix)
    return data


def _rec(children, data, name, prefix):
    if children is None or len(children) <= 0:
        return
    for child in children:
        if child is None:
            return
        if child.tag.__eq__(prefix + name):
            data.append(child.text)
            _rec(child.getchildren(), data, name, prefix)
            continue
        _rec(child.getchildren(), data, name, prefix)


def _create_rsp(action):
    return '{}Response'.format(action)


def validate_rsp(rsp, action):
    if isinstance(rsp, dict):
        logger.error("do action", action, "failed", "reason:", rsp)
        raise RequestError(rsp['status'], rsp[_create_rsp(action)])