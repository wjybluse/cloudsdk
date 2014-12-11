# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request


class VolumeSupport():
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def create_volume(self, name=None, snapshot=None, size=0, **kwargs):
        """
        :param name: the volume name
        :param snapshot: snapshot id ,if snapshot id is not empty,create by it
        :param size:the volume size,if snapshot is not null,use snapshot,otherwise use size
        :param kwargs: other params
        :return:
        """
        pass

    @abc.abstractmethod
    def list_volume(self):
        """
        :return:the all volume
        """
        pass

    @abc.abstractmethod
    def attach_volume(self, instance=None, volume=None, device=None, **kwargs):
        """
        :param instance: instance id
        :param disk: disk id
        :param device: device id like /dev/sda1
        :param kwargs: other params
        :return:
        """
        pass

    @abc.abstractmethod
    def detach_volume(self, instance=None, volume=None):
        """
        :param instance: instance id
        :param disk: disk id
        :return: nothing
        """
        pass

    @abc.abstractmethod
    def remove_volume(self, volume):
        """
        :param volume: volume id
        :return:
        """
        pass

    @abc.abstractmethod
    def query_volume_details(self, volume):
        """
        :param volume: query volume details,volume id
        :return:<volume id,name,size,instances>
        """
        pass


def to_volume(id, name, size, instance):
    return dict(id=id, name=name, size=size, instance=instance)