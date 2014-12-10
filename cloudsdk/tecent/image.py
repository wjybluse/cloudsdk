# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.image import ImageSupport
from _validate import validate_rsp
from _toolbox.logger import LogFactory
# tecent api is so bad,given the api.qcloud.com and ok
# image supported
logger = LogFactory.logger(__name__)


class TecentImageSupport(ImageSupport):
    def __init__(self, ctx):
        setattr(ctx, 'host', 'image.{0}'.format(ctx.host))
        ImageSupport.__init__(self, ctx)

    def list_images(self, image_type=1):
        images = self._images()
        ret = []
        for image in images:
            ret.append(image['imageId'])
        return ret

    def create_image(self, from_snapshot=None, from_instance=None, name=None, **kwargs):
        rsp = self.request.invoke(Action='CreateImage', instanceId=from_instance,
                                  imageName=name)
        validate_rsp(rsp, 'CreateImage')
        images = self._images()
        for image in images:
            if image['imageName'].__eq__(name):
                logger.info("find image", image)
                return image['imageId']
        return None

    def query_image(self, name=None, **kwargs):
        images = self.list_images()
        for image in images:
            if image['imageName'].__eq__(name):
                return image
        return None

    def remove_image(self, image):
        data = {"imageIds.1": image}
        rsp = self.request.invoke(Action='DeleteImages', **data)
        validate_rsp(rsp, 'DeleteImages')

    def _images(self, image_type=1):
        rsp = self.request.invoke(Action='DescribeImages', imageType=image_type)
        validate_rsp(rsp, 'DescribeImages')
        if rsp is None:
            return None
        if 'imageSet' not in rsp:
            logger.error("can not find the images", rsp)
            return None
        images = []
        rsp = eval(rsp)
        for image in eval(rsp)['imageSet']:
            images.append(image)
        return images