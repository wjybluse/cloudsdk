# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.provider import CloudProvider
from instance import TecentInstanceSupport
from security import TecentSecurityGroupSupport
from volume import TecentVolumeSupport
from datacenter import TecentDCSupport
from image import TecentImageSupport
from snapshot import TecentSnapshotSupport
from context import TecentContext


class TecentCloudProvider(CloudProvider):
    def image_support(self):
        return TecentImageSupport(self.ctx)

    def security_support(self):
        return TecentSecurityGroupSupport(self.ctx)

    def instance_support(self):
        return TecentInstanceSupport(self.ctx)

    def volume_support(self):
        return TecentVolumeSupport(self.ctx)

    def snapshot_support(self):
        return TecentSnapshotSupport(self.ctx)

    def dc_support(self):
        return TecentDCSupport(self.ctx)

    @classmethod
    def instance(cls, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        return cls(TecentContext(access_key, secret_key, host=host, port=port, region=region, **kwargs))

