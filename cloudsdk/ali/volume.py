# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.volume import VolumeSupport
from _base import validate_rsp
from _toolbox.logger import log
from cloudsdk.api.volume import to_volume


class AliVolumeSupport(VolumeSupport):
    @log
    def create_volume(self, name=None, snapshot=None, size=0, **kwargs):
        """
        :param zoneId:need
        :return:
        """
        rsp = None
        if snapshot is None:
            rsp = self.request.invoke(Action='CreateDisk', Size=size, **kwargs)
        else:
            rsp = self.request.invoke(Action='CreateDisk', SnapshotId=snapshot, **kwargs)
        validate_rsp(replace_java_keyword(rsp), 'CreateDisk')
        return eval(rsp)['DiskId']

    @log
    def list_volume(self):
        rsp = self.request.invoke(Action='DescribeDisks')
        validate_rsp(rsp, 'DescribeDisks')
        rsp = eval(replace_java_keyword(rsp))
        volumes = eval(rsp)['Disks']
        if volumes is None or len(volumes) <= 0:
            return None
        ret = []
        for volume in volumes['Disk']:
            ret.append(volume['DiskId'])
        return ret


    @log
    def attach_volume(self, instance=None, volume=None, device=None, **kwargs):
        rsp = self.request.invoke(Action='AttachDisk', InstanceId=instance, DiskId=volume, Device=device, **kwargs)
        validate_rsp(rsp, 'AttachDisk')

    @log
    def detach_volume(self, instance=None, volume=None):
        rsp = self.request.invoke(Action='DetachDisk', InstanceId=instance, DiskId=volume)
        validate_rsp(rsp, 'DetachDisk')

    @log
    def remove_volume(self, volume):
        rsp = self.request.invoke(Action='DeleteDisk', DiskId=volume)
        validate_rsp(rsp, 'DeleteDisk')

    def query_volume_details(self, volume):
        rsp = self.request.invoke(Action='DescribeDisks')
        validate_rsp(rsp, 'DescribeDisks')
        rsp = eval(replace_java_keyword(rsp))
        volumes = eval(rsp)['Disks']
        if volumes is None or len(volumes) <= 0:
            return None
        for details in volumes['Disk']:
            if details['DiskId'] == volume:
                return to_volume(volume, details['DiskName'], details['Size'], details['InstanceId'])


def replace_java_keyword(rsp):
    for word in ["true", "false", "null"]:
        rsp = rsp.replace("\\\"" + word + "\\\"", word)
        rsp = rsp.replace(word, "\\\"" + word + "\\\"")
    return rsp


