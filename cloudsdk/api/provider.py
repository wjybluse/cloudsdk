# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc


class CloudProvider():
    def __init__(self, ctx):
        self.ctx = ctx

    @abc.abstractmethod
    def instance_provider(self):
        pass

    @abc.abstractmethod
    def image_support(self):
        pass

    @abc.abstractmethod
    def dc_support(self):
        pass

    @abc.abstractmethod
    def snapshot_support(self):
        pass

    @abc.abstractmethod
    def security_support(self):
        pass

    @abc.abstractmethod
    def volume_support(self):
        pass

    @classmethod
    def instance(cls, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        raise NotImplementedError("The method not implement")