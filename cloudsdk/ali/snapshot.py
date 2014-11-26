# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.snapshot import SnapshotSupport


class AliSnapshotSupport(SnapshotSupport):
    def list_snapshot(self, instance=None, disk=None, **kwargs):
        rsp = self.request.invoke(Aciton='DescribeSnapshots', InstanceId=instance, **kwargs)
        if rsp is None:
            return None
        rsp = eval(eval(rsp))
        if len(rsp['Snapshots']) <= 0:
            return None
        snapshots = []
        for snapshot in rsp['Snapshots']['SnapshotResource']:
            snapshots.append(snapshot)
        return snapshots

    def create_snapshot(self, disk=None, name=None, **kwargs):
        rsp = self.request.invoke(Action='CreateSnapshot', DiskId=disk, SnapshotName=name, **kwargs)
        return eval(rsp)['SnapshotId']
