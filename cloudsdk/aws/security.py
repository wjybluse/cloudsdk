# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.security import SecurityGroupSupport
from _xml import XmlParser
from _xml import validate_rsp
from _xml import find_all


class AWSSecurityGroupSupport(SecurityGroupSupport):
    def __init__(self, ctx):
        SecurityGroupSupport.__init__(self, ctx)
        ctx.service_name = 'ec2'

    def create_security_group(self, name=None, description=None, **kwargs):
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='CreateSecurityGroup',
                                  GroupName=name,
                                  GroupDescription=description)
        validate_rsp(rsp, 'CreateSecurityGroup')
        return find_all(rsp, 'groupId')

    def list_security_group(self):
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='DescribeSecurityGroups')
        validate_rsp(rsp, 'DescribeSecurityGroups')
        return find_all(rsp, 'groupId')