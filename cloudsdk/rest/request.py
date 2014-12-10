# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.rest.rest import RestClient
from _toolbox.error import RequestError
from _toolbox.logger import LogFactory

logger = LogFactory.logger(__name__)


class Request():
    def __init__(self, ctx):
        self.ctx = ctx

    def invoke(self, scheme='https', callback=None, **kwargs):
        client = None
        try:
            logger.debug("invoke request", "params", kwargs)
            client = RestClient(scheme=scheme, host=self.ctx.host, port=self.ctx.port)
            url = self.ctx.get_context()(**kwargs)
            rsp = client.add_headers(**self.ctx.get_headers()).get(url=url, callback=callback)
            logger.info("Response message", rsp)
            if isinstance(rsp, dict) and 'status' in rsp:
                status = rsp['status']
                raise RequestError(status, rsp['message'])
            return rsp
        finally:
            client.close()