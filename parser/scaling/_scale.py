# -*- coding: utf-8 -*-
# context contains all scaling rule if it is autoscaling
# if manual ,the context contains only cloud information
__author__ = 'wan'
from cloudsdk.tool.logger import LogFactory

logger = LogFactory.logger(__file__)


class ScaleController():
    def __init__(self, ctx):
        """
        :param ctx:ScaleContext,include cloud name,and other cloud information
        :return:
        """
        self.ctx = ctx

    def scaling(self):
        name = self.ctx.cloud_name
        if name is None or len(name) <= 0:
            raise ValueError("cloud name can not empty")
        server_type = self.ctx.server_type
        if server_type is None or len(server_type) <= 0:
            logger.warn("Can not find the server type,exit")
            return
        cls_name = "{0}CloudProvider".format(name.capitalize())
        module = __import__("cloudsdk.{0}.provider".format(name), fromlist=[cls_name])
        provider = getattr(module, cls_name)(self.ctx.access_key, self.ctx.access_secret, host=self.ctx.host,
                                             port=self.ctx.port, region=self.ctx.region, **self.ctx.kwargs)
        # how to scale
        # query image id from db,filter {cloud_name,image_type},flavor,bandwidth for ali and tecent,and other params
        image_id = ""
        flavor = ""
        bandwidth = ""
        other_params = {}
        instance_id = provider.instance_support().launch(image=image_id, flavor=flavor, hostname='evh',
                                                         bandwidth=bandwidth,
                                                         **other_params)
        save_instance(instance_id, name)


def save_instance(instance, cloud_name):
    """
    :param instance: instance id
    :param cloud_name: create from which cloud
    :return: nothing
    """
    pass
