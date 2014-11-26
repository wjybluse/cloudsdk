# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request


class DCSupport():
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def list_regions(self):
        """
        :return:region list
        """
        pass

    @abc.abstractmethod
    def list_zones(self):
        """
        :param region: region id
        :return: zone list
        """
        pass