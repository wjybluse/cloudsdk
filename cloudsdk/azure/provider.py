# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.provider import CloudProvider
from instance import AzureInstanceSupport
from security import AzureSecurityGroupSupport
from volume import AzureVolumeSupport
from datacenter import AzureDCSupport
from image import AzureImageSupport
from snapshot import AzureSnapshotSupport
from context import AzureContext


class AzureCloudProvider(CloudProvider):
    def image_support(self):
        return AzureImageSupport(self.ctx)

    def security_support(self):
        return AzureSecurityGroupSupport(self.ctx)

    def instance_provider(self):
        return AzureInstanceSupport(self.ctx)

    def volume_support(self):
        return AzureVolumeSupport(self.ctx)

    def snapshot_support(self):
        return AzureSnapshotSupport(self.ctx)

    def dc_support(self):
        return AzureDCSupport(self.ctx)

    @classmethod
    def instance(cls, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        return cls(AzureContext(access_key, secret_key, host=host, port=port, region=region, **kwargs))
