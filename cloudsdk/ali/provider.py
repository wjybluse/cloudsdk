# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.provider import CloudProvider
from instance import AliInstanceSupport
from security import AliSecurityGroupSupport
from volume import AliVolumeSupport
from datacenter import AliDCSupport
from image import AliImageSupport
from snapshot import AliSnapshotSupport
from context import AliContext


class AliCloudProvider(CloudProvider):
    def image_support(self):
        return AliImageSupport(self.ctx)

    def security_support(self):
        return AliSecurityGroupSupport(self.ctx)

    def instance_support(self):
        return AliInstanceSupport(self.ctx)

    def volume_support(self):
        return AliVolumeSupport(self.ctx)

    def snapshot_support(self):
        return AliSnapshotSupport(self.ctx)

    def dc_support(self):
        return AliDCSupport(self.ctx)

    @classmethod
    def instance(cls, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        return cls(AliContext(access_key, secret_key, host=host, port=port, region=region, **kwargs))
