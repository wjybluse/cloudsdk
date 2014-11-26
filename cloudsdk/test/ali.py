# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from cloudsdk.ali.image import AliImageSupport
from cloudsdk.ali.context import AliContext
from cloudsdk.ali.datacenter import AliDCSupport

KEY_ID = 'your key'
KEY_SECRET = 'your secret'


class AliCloudTest(unittest.TestCase):
    def test_query_images(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=80, region='cn-shenzhen')
        images = AliImageSupport(cxt)
        all = images.list_images()
        self.assertIsNotNone(all)

    def test_list_region(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=80, region='cn-shenzhen')
        region = AliDCSupport(cxt)
        ret = region.list_regions()
        print(ret)
        self.assertIsNotNone(ret)

    def test_list_zone(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=80, region='cn-shenzhen')
        region = AliDCSupport(cxt)
        ret = region.list_zones()
        print(ret)
        self.assertIsNotNone(ret)


