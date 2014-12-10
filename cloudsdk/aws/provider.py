# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.provider import CloudProvider
from instance import AWSInstanceSupport
from security import AWSSecurityGroupSupport
from volume import AWSVolumeSupport
from datacenter import AWSDCSupport
from image import AWSImageSupport
from snapshot import AWSSnapshotSupport
from context import AWSContext


class AwsCloudProvider(CloudProvider):
    def image_support(self):
        return AWSImageSupport(self.ctx)

    def security_support(self):
        return AWSSecurityGroupSupport(self.ctx)

    def instance_support(self):
        return AWSInstanceSupport(self.ctx)

    def volume_support(self):
        return AWSVolumeSupport(self.ctx)

    def snapshot_support(self):
        return AWSSnapshotSupport(self.ctx)

    def dc_support(self):
        return AWSDCSupport(self.ctx)

    @classmethod
    def instance(cls, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        return cls(AWSContext(access_key, secret_key, host=host, port=port, region=region, **kwargs))