# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.instance import InstanceSupport

FORCE = dict(True='true', False='false')


class AliInstanceSupport(InstanceSupport):
    def launch(self, image=None, flavor=None, hostname=None, bandwidth=None, callback=None, **kwargs):
        rsp = self.request.invoke(action='CreateInstance', hostname=hostname, ImageId=image,
                                  InternetMaxBandwidthOut=bandwidth, InstanceType=flavor,
                                  **kwargs)
        return eval(rsp)['InstanceId']

    def start(self, instance):
        self.request.invoke(Action='StartInstance', InstanceId=instance)

    def stop(self, instance, force=False):
        self.request.invoke(Action='StopInstance', InstanceId=instance, ForceStop=FORCE[force])

    def remove(self, instance):
        self.request.invoke(Action='DeleteInstance', InstanceId=instance)

    def list_instances(self):
        rsp = self.request.invoke(Action='DescribeInstanceStatus')
        if rsp is None:
            return None
        rsp = eval(rsp)
        status = eval(rsp)['InstanceStatuses']
        if status is None:
            return None
        ret = status['InstanceStatus']
        if len(ret) <= 0:
            return None
        instances = []
        for instance in ret:
            instances.append(instance)
        return instances

