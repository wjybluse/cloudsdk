# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.instance import InstanceSupport
from _xml import XmlParser
from _xml import find_all
from _xml import validate_rsp


class AWSInstanceSupport(InstanceSupport):
    def __init__(self, ctx):
        InstanceSupport.__init__(self, ctx)
        ctx.service_name = 'ec2'

    def launch(self, image=None, flavor=None, hostname=None, bandwidth=None, **kwargs):
        """
        :param image: image id
        :param flavor: InstanceType
        :param hostname: host name,not valid
        :param bandwidth: not valid
        :param kwargs: MaxCount,MinCount,KeyName
        :return:
        """
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='RunInstances', ImageId=image,
                                  MaxCount=1,
                                  MinCount=1, InstanceType=flavor, **kwargs)
        validate_rsp(rsp, 'RunInstances')
        return find_all(rsp, 'instanceId')

    def start(self, instance):
        data = {'InstanceId.1': instance}
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='StartInstances', **data)
        validate_rsp(rsp, 'StartInstances')

    def stop(self, instance, force=False):
        data = {'InstanceId.1': instance}
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='TerminateInstances', **data)
        validate_rsp(rsp, 'TerminateInstances')

    def list_instances(self):
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='DescribeInstances')
        validate_rsp(rsp, 'DescribeInstances')
        return find_all(rsp, 'instanceId')

    def remove(self, instance):
        data = {'InstanceId.1': instance}
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='StopInstances', **data)
        validate_rsp(rsp, 'StopInstances')
