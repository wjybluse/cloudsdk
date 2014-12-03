# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.security import SecurityGroupSupport


class AzureSecurityGroupSupport(SecurityGroupSupport):
    def create_security_group(self, name=None, description=None, **kwargs):
        pass

    def list_security_group(self):
        pass
