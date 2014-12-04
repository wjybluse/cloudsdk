# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.instance import InstanceSupport
from cloudsdk.tool.logger import LogFactory

logger = LogFactory.logger(__name__)


class TecentInstanceSupport(InstanceSupport):
    def __init__(self, ctx):
        setattr(ctx, 'host', "cvm.{0}".format(ctx.host))
        InstanceSupport.__init__(self, ctx)

    def launch(self, image=None, flavor=None, hostname=None, bandwidth=None, **kwargs):
        """
        :param image: image id
        :param flavor: not valid
        :param hostname: not valid
        :param bandwidth:
        :param kwargs: cpu,ram,size,period
        :return:
        """
        self.request.invoke(Action='RunInstances', imageId=image, imageType=1, **kwargs)

    def start(self, instance):
        data = {"instanceIds.1": instance}
        self.request.invoke(Action='StartInstances', **data)

    def stop(self, instance, force=False):
        data = {"instanceIds.1": instance}
        self.request.invoke(Action='StopInstances', **data)

    def remove_instance(self, instance):
        data = {"instanceIds.1": instance}
        self.request.invoke(Action='TerminateInstances', **data)

    def list_instances(self):
        rsp = self.request.invoke(Action='DescribeInstances')
        logger.debug("The response is", rsp)
        if 'instanceSet' not in rsp:
            return None
        instances = []
        rsp = eval(rsp)
        for instance in eval(rsp)['instanceSet']:
            instances.append(instance)
        return instances
