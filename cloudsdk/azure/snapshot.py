# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.ali.snapshot import SnapshotSupport
from _common import BaseSupport


class AzureSnapshotSupport(SnapshotSupport):
    def __init__(self, ctx):
        self.ctx = ctx
        self.azure = BaseSupport.instance(self.ctx.access_key).service_management

    def list_snapshot(self, instance=None, disk=None, **kwargs):
        raise NotImplementedError("the cloud can not support this method")

    def create_snapshot(self, disk=None, name=None, **kwargs):
        raise NotImplementedError("the cloud can not support this method")
