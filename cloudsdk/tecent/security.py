# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.security import SecurityGroupSupport


class TecentSecurityGroupSupport(SecurityGroupSupport):
    def create_security_group(self, name=None, description=None, **kwargs):
        raise NotImplementedError("Qcloud does not support this method")

    def list_security_group(self):
        raise NotImplementedError("Qcloud does not support this method")