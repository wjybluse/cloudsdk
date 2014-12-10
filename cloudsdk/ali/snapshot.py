# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.snapshot import SnapshotSupport
from _base import validate_rsp
from _toolbox.logger import log

class AliSnapshotSupport(SnapshotSupport):
    @log
    def list_snapshot(self, instance=None, disk=None, **kwargs):
        rsp = self.request.invoke(Aciton='DescribeSnapshots', InstanceId=instance, **kwargs)
        validate_rsp(rsp, 'DescribeSnapshots')
        rsp = eval(eval(rsp))
        if len(rsp['Snapshots']) <= 0:
            return None
        snapshots = []
        for snapshot in rsp['Snapshots']['SnapshotResource']:
            snapshots.append(snapshot['SnapshotId'])
        return snapshots

    @log
    def create_snapshot(self, disk=None, name=None, **kwargs):
        rsp = self.request.invoke(Action='CreateSnapshot', DiskId=disk, SnapshotName=name, **kwargs)
        validate_rsp(rsp, 'CreateSnapshot')
        return eval(rsp)['SnapshotId']

    @log
    def remove_snapshot(self, snapshot):
        rsp = self.request.invoke(Action='DeleteSnapshot', SnapshotId=snapshot)
        validate_rsp(rsp, 'DeleteSnapshot')
