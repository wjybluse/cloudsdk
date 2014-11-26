# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from cloudsdk.ali.image import AliImageSupport
from cloudsdk.ali.context import AliContext

KEY_ID = 'ldQ2leJaGVQYFxx4'
KEY_SECRET = 'rdGRencqiPRA4OhazHQSdJepRBg2Tv'


class AliCloudTest(unittest.TestCase):
    def test_query_images(self):
        cxt = AliContext(KEY_ID, KEY_SECRET, host='ecs.aliyuncs.com', port=80, region='cn-shenzhen')
        images = AliImageSupport(cxt)
        all = images.list_images()
        self.assertIsNotNone(all)



