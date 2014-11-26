# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.snapshot import SnapshotSupport


class AWSSnapshotSupport(SnapshotSupport):
    def __init__(self, ctx):
        pass

    def list_snapshot(self, instance=None, disk=None, **kwargs):
        raise NotImplementedError("The method not implement")

    def create_snapshot(self, disk=None, name=None, **kwargs):
        raise NotImplementedError("The method not implement")
