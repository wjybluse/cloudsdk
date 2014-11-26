# -*- coding: utf-8 -*-
__author__ = 'wan'
from instance import InstanceSupport
from image import ImageSupport
from datacenter import DCSupport
from snapshot import SnapshotSupport


class CloudProvider():
    instance = None

    def __init__(self, ctx):
        self.ctx = ctx

    def instance_provider(self):
        return InstanceSupport(self.ctx)

    def image_support(self):
        return ImageSupport(self.ctx)

    def dc_support(self):
        return DCSupport(self.ctx)

    def snapshot_support(self):
        return SnapshotSupport(self.ctx)

    @classmethod
    def instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance