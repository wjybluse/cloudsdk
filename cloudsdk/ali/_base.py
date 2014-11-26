# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.tool.logger import LogFactory
from cloudsdk.rest.request import RequestError

logger = LogFactory.logger(__name__)


def validate_rsp(rsp, action):
    if isinstance(rsp, dict) and 'message' in rsp:
        logger.error("Error", rsp, "action=", action)
        raise RequestError(rsp['status'], rsp['message'])
