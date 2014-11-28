# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.volume import VolumeSupport
from cloudsdk.rest.request import RequestError
from _xml import XmlParser
from _xml import validate_rsp
from _xml import find_all


class AWSVolumeSupport(VolumeSupport):
    def __init__(self, ctx):
        VolumeSupport.__init__(self, ctx)
        ctx.service_name = 'ec2'

    def create_volume(self, name=None, snapshot=None, size=0, **kwargs):
        rsp = None
        if snapshot is not None or len(snapshot) > 0:
            rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='CreateVolume',
                                      SnapshotId=snapshot,
                                      **kwargs)
        elif size > 0:
            rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='CreateVolume', Size=size,
                                      **kwargs)
        else:
            raise RequestError(400, 'Invalid Request')
        validate_rsp(rsp, 'CreateVolume')
        return find_all(rsp, 'volumeId')[0]


    def list_volume(self):
        rsp = self.request.invoke(scheme='https', Action='DescribeVolumes', callback=XmlParser.parser)
        validate_rsp(rsp, 'DescribeVolumes')
        return find_all(rsp, 'volumeId')


    def attach_volume(self, instance=None, volume=None, device=None, **kwargs):
        rsp = self.request.invoke(scheme='https', Action='AttachVolume', callback=XmlParser.parser, InstanceId=instance,
                                  VolumeId=volume, **kwargs)
        validate_rsp(rsp, 'AttachVolume')


    def detach_volume(self, instance=None, volume=None):
        rsp = self.request.invoke(scheme='https', Action='DetachVolume', callback=XmlParser.parser,
                                  InstanceId=instance,
                                  VolumeId=volume)
        validate_rsp(rsp, 'DetachVolume')
