# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.volume import VolumeSupport
from _common import BaseSupport


class AzureVolumeSupport(VolumeSupport):
    def __init__(self, ctx):
        self.azure = BaseSupport.instance(ctx.access_key).service_management
        self.ctx = ctx

    def create_volume(self, name=None, snapshot=None, size=0, **kwargs):
        """
        :param name: volume name
        :param snapshot: like media_link
        :param size: not used
        :param kwargs:media_link the path
        :return:data object
        """
        return self.azure.add_disk(False, name, kwargs['media_link'], name, "Linux")

    def detach_volume(self, instance=None, volume=None):
        self.azure.delete_data_disk(self.ctx.service_name, instance, volume, 0, delete_vhd=False)

    def attach_volume(self, instance=None, volume=None, device=None, **kwargs):
        self.azure.add_data_disk(self, self.ctx.service_name, instance, volume, 0,
                                 host_caching=None, media_link=None, disk_label=volume,
                                 disk_name=volume, logical_disk_size_in_gb=kwargs['size'],
                                 source_media_link=None)


    def list_volume(self):
        return self.azure.list_disks()
