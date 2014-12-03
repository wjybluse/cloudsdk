# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from cloudsdk.ali.image import AliImageSupport
from cloudsdk.ali.context import AliContext
from cloudsdk.ali.datacenter import AliDCSupport
from cloudsdk.ali.instance import AliInstanceSupport
from cloudsdk.ali.volume import AliVolumeSupport
from cloudsdk.ali.security import AliSecurityGroupSupport
from cloudsdk.ali.provider import AliCloudProvider

KEY_ID = 'ldQ2leJaGVQYFxx4'
KEY_SECRET = 'rdGRencqiPRA4OhazHQSdJepRBg2Tv'


class AliCloudTest(unittest.TestCase):
    def test_query_images(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        images = AliImageSupport(cxt)
        all = images.list_images()
        self.assertIsNotNone(all)

    def test_list_region(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        region = AliDCSupport(cxt)
        ret = region.list_regions()
        print(ret)
        self.assertIsNotNone(ret)

    def test_list_zone(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        region = AliDCSupport(cxt)
        ret = region.list_zones()
        print(ret)
        self.assertIsNotNone(ret)

    def test_remove_instance(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        instance = AliInstanceSupport(cxt)
        instance.remove('i-94dqulg0q')

    def test_create_instance(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        instance = AliInstanceSupport(cxt)
        rsp = instance.launch(image='m-94fdnlshi', flavor='ecs.t1.xsmall', SecurityGroupId='sg-94meu1xof')
        self.assertIsNotNone(rsp)

    def test_list_volume(self):
        # 用不了
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        volume = AliVolumeSupport(cxt)
        ret = volume.list_volume()
        print(ret)
        self.assertIsNotNone(ret)

    def test_create_volume(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        volume = AliVolumeSupport(cxt)
        ret = volume.create_volume(name='wantest', size=5, ZoneId='cn-shenzhen-st3004-a')
        print(ret)
        self.assertIsNotNone(ret)

    def test_list_sg(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        sg = AliSecurityGroupSupport(cxt)
        ret = sg.list_security_group()
        print(ret)
        self.assertIsNotNone(ret)

    def test_create_sg(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443, region='cn-shenzhen')
        sg = AliSecurityGroupSupport(cxt)
        ret = sg.create_security_group(name='wantest', description='wanwan')
        print(ret)
        self.assertIsNotNone(ret)

    def test_provider(self):
        provider = AliCloudProvider.instance(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=443,
                                             region='cn-shenzhen')
        ret = provider.image_support().list_images()
        self.assertIsNotNone(ret)
        print(ret)

