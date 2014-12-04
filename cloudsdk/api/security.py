# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request


class SecurityGroupSupport():
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def create_security_group(self, name=None, description=None, **kwargs):
        """
        :param name: name of security group
        :param description: desc
        :param kwargs: other information
        :return:
        """
        pass

    @abc.abstractmethod
    def list_security_group(self):
        """
        :return:security group id
        """
        pass

    @abc.abstractmethod
    def remove_security_group(self, group):
        """
        :param group: group id
        :return:
        """
        pass