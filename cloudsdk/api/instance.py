# -*- coding: utf-8 -*-
__author__ = 'wan'
# the class provider the instance support
# ctx provider the auth information
import abc
from cloudsdk.rest.request import Request


class InstanceSupport(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def launch(self, image=None, flavor=None, hostname=None, bandwidth=None, **kwargs):
        """
        :param image:  image id
        :param flavor:  flavor,the cpu,ram ,disk of the vm
        :param hostname: host name
        :param bandwidth:
        :param kwargs: other params like security group,key pair and so on
        :return:instance id, if callback is not none,return callback(instance id)
        """
        pass

    @abc.abstractmethod
    def start(self, instance):
        """
        :param instance: instance id
        :return:
        """
        pass

    @abc.abstractmethod
    def stop(self, instance, force=False):
        """
        :param instance: instance id
        :param force force stop
        :return:
        """
        pass

    @abc.abstractmethod
    def remove_instance(self, instance):
        """
        :param instance: instance id
        :return:
        """
        pass

    @abc.abstractmethod
    def list_instances(self):
        """
        :return:return all instance created
        """
        pass
