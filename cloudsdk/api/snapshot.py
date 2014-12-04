# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request
# The interface support create and list snapshot


class SnapshotSupport():
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def create_snapshot(self, disk=None, name=None, **kwargs):
        """
        :param disk:disk id ,the image create in
        :param name:snapshot name,[option]
        :param kwargs: advance params
        :return:
        """
        pass

    @abc.abstractmethod
    def list_snapshot(self, instance=None, disk=None, **kwargs):
        """
        :param instance: instance id
        :param disk: disk id [option]
        :param region: region
        :param kwargs: advance params
        :return:
        """
        pass

    @abc.abstractmethod
    def remove_snapshot(self, snapshot):
        """
        :param snapshot: snapshot id
        :return:
        """
        pass