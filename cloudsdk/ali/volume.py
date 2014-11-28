# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.volume import VolumeSupport
from _base import validate_rsp
# 阿里接口调不通，可能有限制
#现在正在解决

class AliVolumeSupport(VolumeSupport):
    def create_volume(self, name=None, snapshot=None, size=0, **kwargs):
        """
        :param zoneId:need
        :return:
        """
        rsp = self.request.invoke(Action='CreateDisk', SnapshotId=snapshot, Size=size, **kwargs)
        validate_rsp(rsp)
        return eval(rsp)['DiskId']

    def list_volume(self):
        rsp = self.request.invoke(Action='DescribeDisks')
        validate_rsp(rsp, 'DescribeDisks')
        rsp = eval(rsp)
        volumes = eval(rsp)['Disks']
        if volumes is None or len(volumes) <= 0:
            return None
        ret = []
        for volume in volumes['Disk']:
            ret.append(volume)
        return ret


    def attach_volume(self, instance=None, volume=None, device=None, **kwargs):
        rsp = self.request.invoke(Action='AttachDisk', InstanceId=instance, DiskId=volume, Device=device, **kwargs)
        validate_rsp(rsp, 'DescribeDisks')

    def detach_volume(self, instance=None, volume=None):
        rsp = self.request.invoke(Action='DetachDisk', InstanceId=instance, DiskId=volume)
        validate_rsp(rsp, 'DescribeDisks')