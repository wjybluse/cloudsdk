# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request


class ImageSupport():
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def list_images(self, image_type=1):
        """
        :param image_type:current support private and public 1 or 2
        :return:
        """
        pass

    @abc.abstractmethod
    def create_image(self, from_snapshot=None, from_instance=None, name=None, **kwargs):
        """
        :param from_instance:from ali instance copy
        :param from_snapshot:snapshot of image
        :param disk:the disk
        :param dc: data center or region
        :param kwargs: advance params
        :return:image id
        """
        pass

    @abc.abstractmethod
    def query_image(self, name=None):
        """
        :param name: image name
        :return:
        """
        pass