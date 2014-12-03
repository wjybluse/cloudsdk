# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.image import ImageSupport
from _common import BaseSupport
from azure.servicemanagement import *


class AzureImageSupport(ImageSupport):
    def __init__(self, ctx):
        self.ctx = ctx
        self.azure = BaseSupport.instance(self.ctx.access_key).service_management

    def list_images(self, image_type=1):
        return self.azure.list_os_images()


    def create_image(self, from_snapshot=None, from_instance=None, name=None, **kwargs):
        # can not understand
        vm_image = VMImage(name=name, label=name)
        return self.azure.create_os_image(vm_image)

    def query_image(self, name=None):
        pass
