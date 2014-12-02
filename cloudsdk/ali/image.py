# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.image import ImageSupport


class AliImageSupport(ImageSupport):
    def create_image(self, from_snapshot=None, from_instance=None, name=None, dc=None, **kwargs):
        rsp = self.request.invoke(Action='CreateImage', SnapshotId=from_snapshot, ImageName=name, **kwargs)
        return eval(rsp)['ImageId']

    def query_image(self, name=None):
        images = self._list_images()
        if images is None:
            return None
        for image in images:
            if image['ImageName'].__eq__(name):
                return image

    def list_images(self, image_type=1):
        data = []
        images = self._list_images()
        if images is None:
            return None
        for image in images:
            data.append(image)
        return data

    def _list_images(self):
        rsp = self.request.invoke(Action='DescribeImages')
        if rsp is None:
            return None
        rsp = eval(rsp.replace("true", "\\\"true\\\"").replace("false", "\\\"false\\\""))
        if eval(rsp)['Images'] is None:
            return None
        return eval(rsp)['Images']['Image']