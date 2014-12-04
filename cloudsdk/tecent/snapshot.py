# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.snapshot import SnapshotSupport


class TecentSnapshotSupport(SnapshotSupport):
    def list_snapshot(self, instance=None, disk=None, **kwargs):
        raise NotImplementedError("The qcloud not support the method")

    def create_snapshot(self, disk=None, name=None, **kwargs):
        raise NotImplementedError("The qcloud not support the method")

    def remove_snapshot(self, snapshot):
        raise NotImplementedError("The qcloud not support the method")

