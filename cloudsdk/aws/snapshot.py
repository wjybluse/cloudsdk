# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.snapshot import SnapshotSupport
from _xml import XmlParser
from _xml import validate_rsp
from _xml import find_all


class AWSSnapshotSupport(SnapshotSupport):
    def __init__(self, ctx):
        SnapshotSupport.__init__(self, ctx)
        ctx.service_name = 'ec2'

    def list_snapshot(self, instance=None, disk=None, **kwargs):
        rsp = self.request.invoke(callback=XmlParser.parser, Action='DescribeSnapshots')
        validate_rsp(rsp)
        return find_all(rsp, "snapshotId")


    def create_snapshot(self, disk=None, name=None, **kwargs):
        rsp = self.request.invoke(callback=XmlParser.parser, Action='CreateSnapshot', VolumeId=disk, **kwargs)
        validate_rsp(rsp)
        return find_all(rsp, "snapshotId")

    def remove_snapshot(self, snapshot):
        rsp = self.request.invoke(callback=XmlParser.parser, Action='DeleteSnapshot', SnapshotId=snapshot)
        validate_rsp(rsp)
