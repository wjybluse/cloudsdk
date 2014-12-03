# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.datacenter import DCSupport
from _validate import validate_rsp


class TecentDCSupport(DCSupport):
    def __init__(self, ctx):
        setattr(ctx, 'host', 'trade.{0}'.format(ctx.host))
        DCSupport.__init__(self, ctx)

    def list_regions(self):
        rsp = self.request.invoke(Action='DescribeProductRegionList', instanceType=1)
        validate_rsp(rsp, 'DescribeProductRegionList')
        rsp = eval(rsp)
        return eval(rsp)['availableRegion'].keys()

    def list_zones(self):
        raise NotImplementedError("The qcloud does not support the method")
