# Autoscale support
# support ali cloud,aws
# monitor by self
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request


class AutoScaling():
    def __init__(self, context):
        self.context = context
        self.request = Request(context)

    @abc.abstractmethod
    def create_scaling_group(self, name, max, min, **kwargs):
        """
        :param name: group name
        :param max: max instance
        :param min: min instance
        :param kwargs: other like default cooldown,removalpolicy,loadbalance
        :return:
        """
        pass

    @abc.abstractmethod
    def list_scaling_groups(self):
        """
        :return:all created _scaling group
        """
        pass

    @abc.abstractmethod
    def active_scaling_group(self, group):
        """
        :param group: group id
        :return:
        """
        pass

    @abc.abstractmethod
    def unactive_scaling_group(self, group):
        """
        :param group: group id
        :return:
        """
        pass

    @abc.abstractmethod
    def remove_scaling_group(self, group):
        """
        :param group:   group id
        :return:
        """
        pass

