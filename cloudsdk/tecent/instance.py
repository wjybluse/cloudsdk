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
        self.request.invoke(scheme='https', Action='RunInstances', imageId=image, cpu=kwargs['cpu'],
                            mem=kwargs['ram'],
                            storageSize=kwargs['size'], period=kwargs['period'])

    def start(self, instance):
        data = {"instanceIds.1": instance}
        self.request.invoke(scheme='https', Action='StartInstances', **data)

    def stop(self, instance, force=False):
        data = {"instanceIds.1": instance}
        self.request.invoke(scheme='https', Action='StopInstances', **data)

    def remove(self, instance):
        data = {"instanceIds.1": instance}
        self.request.invoke(scheme='https', Action='TerminateInstances', **data)

    def list_instances(self):
        rsp = self.request.invoke(scheme='https', Action='DescribeInstances')
        logger.debug("The response is", rsp)
        if 'instanceSet' not in rsp:
            return None
        instances = []
        rsp = eval(rsp)
        for instance in eval(rsp)['instanceSet']:
            instances.append(instance)
        return instances
