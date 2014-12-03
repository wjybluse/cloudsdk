# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.tool.logger import LogFactory
from cloudsdk.rest.request import RequestError

logger = LogFactory.logger(__name__)


def validate_rsp(rsp, action):
    if isinstance(rsp, dict):
        logger.error("Response message:", rsp, "current action", action)
        raise RequestError(rsp['status'], rsp['message'])
    rsp = eval(eval(rsp))
    code = rsp['code']
    if not str(code).__eq__('0'):
        logger.error("Response message:", rsp, "current action", action)
        raise RequestError(rsp['code'], rsp['message'])
