# -*- coding: utf-8 -*-
# Data object
__author__ = 'wan'
from parser.common.config import ConfigUtil


class ScaleContext():
    def __init__(self, cloud_name, server_type, **kwargs):
        """
        :param cloud_name:cloud provider name,support ali,tecent,aws,azure
        :param server_type:scale type,everhomes,redis,mysql
        :param kwargs:other auth params
        :return:data object
        """
        cfg = ConfigUtil()
        self.cloud_name = cloud_name
        self.server_type = server_type
        self.access_key = cfg.get_value(cloud_name, 'access_key')
        self.access_secret = cfg.get_value(cloud_name, 'access_secret')
        self.host = cfg.get_value(cloud_name, 'host')
        self.port = cfg.get_value(cloud_name, 'port')
        self.region = cfg.get_value(cloud_name, 'region')
        self.kwargs = kwargs
