# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.volume import VolumeSupport


class TecentVolumeSupport(VolumeSupport):
    def create_volume(self, name=None, snapshot=None, size=0, **kwargs):
        raise NotImplementedError("Qcloud does not support this method")

    def list_volume(self):
        raise NotImplementedError("Qcloud does not support this method")

    def attach_volume(self, instance=None, volume=None, device=None, **kwargs):
        raise NotImplementedError("Qcloud does not support this method")

    def detach_volume(self, instance=None, volume=None):
        raise NotImplementedError("Qcloud does not support this method")