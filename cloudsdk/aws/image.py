# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.image import ImageSupport
from cloudsdk.rest.request import Request
from _xml import XmlParser
from cloudsdk.tool.logger import LogFactory
from _xml import find_all
from _xml import validate_rsp

logger = LogFactory.logger(__name__)


class AWSImageSupport(ImageSupport):
    def __init__(self, ctx):
        ImageSupport.__init__(self, ctx)
        ctx.service_name = 'ec2'

    def list_images(self, image_type=1):
        data = {}
        if image_type == 1:
            data['Filter.1.Name'] = 'is-public'
            data['Filter.1.Value.1'] = 'false'
        rsp = self.request.invoke(callback=XmlParser.parser, Action='DescribeImages', **data)
        validate_rsp(rsp, 'DescribeImages')
        return find_all(rsp, 'imageId')

    def create_image(self, from_snapshot=None, from_instance=None, name=None, **kwargs):
        rsp = self.request.invoke(callback=XmlParser.parser, Action='CreateImage',
                                  InstanceId=from_instance, Name=name)
        validate_rsp(rsp, 'CreateImage')
        return find_all(rsp, 'imageId')

    def query_image(self, name=None, **kwargs):
        rsp = self.request.invoke(callback=XmlParser.parser, Action='DescribeImages')
        validate_rsp(rsp, 'DescribeImages')
        return find_all(rsp, 'imageName')


