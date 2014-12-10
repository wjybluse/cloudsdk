# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.security import SecurityGroupSupport
from _base import validate_rsp
from _toolbox.logger import log


class AliSecurityGroupSupport(SecurityGroupSupport):
    @log
    def create_security_group(self, name=None, description=None, **kwargs):
        rsp = self.request.invoke(Action='CreateSecurityGroup', Description=description, **kwargs)
        validate_rsp(rsp, 'CreateSecurityGroup')
        rsp = eval(rsp)
        return eval(rsp)['SecurityGroupId']

    @log
    def list_security_group(self):
        rsp = self.request.invoke(Action='DescribeSecurityGroups')
        validate_rsp(rsp, 'DescribeSecurityGroups')
        rsp = eval(rsp)
        sgs = eval(rsp)['SecurityGroups']
        if sgs is None or len(sgs) <= 0:
            return None
        items = sgs['SecurityGroup']
        security = []
        for item in items:
            security.append(item['SecurityGroupId'])
        return security

    @log
    def remove_security_group(self, group):
        rsp = self.request.invoke(Action='DeleteSecurityGroup', SecurityGroupId=group)
        validate_rsp(rsp, 'DeleteSecurityGroup')
