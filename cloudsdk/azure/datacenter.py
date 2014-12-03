# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.datacenter import DCSupport
from _common import BaseSupport


class AzureDCSupport(DCSupport):
    def __init__(self, ctx):
        self.ctx = ctx
        self.azure = BaseSupport.instance(self.ctx.access_key).service_management

    def list_regions(self):
        return self.azure.list_locations()

    def list_zones(self):
        raise NotImplementedError("not implement by this cloud")
