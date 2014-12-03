__author__ = 'wan'
import unittest
from cloudsdk.tecent.instance import TecentInstanceSupport
from cloudsdk.tecent.context import TecentContext
from cloudsdk.tecent.image import TecentImageSupport
from cloudsdk.tecent.datacenter import TecentDCSupport

KEY_ID = ''
KEY_SECRET = ''


class TestTecent(unittest.TestCase):
    def test_query_instances(self):
        cxt = TecentContext(KEY_ID, KEY_SECRET, host='api.qcloud.com', port=443, region='gz')
        instance = TecentInstanceSupport(cxt)
        ret = instance.list_instances()
        self.assertIsNotNone(ret)
        print(ret)

    def test_query_image(self):
        cxt = TecentContext(KEY_ID, KEY_SECRET,
                            host='api.qcloud.com', port=443, region='gz')
        image = TecentImageSupport(cxt)
        ret = image.list_images()
        self.assertIsNotNone(ret)

    def test_create_image(self):
        id = 'qcvmfa85f0497c33536dc641eaed5c4e3818'
        cxt = TecentContext(KEY_ID, KEY_SECRET,
                            host='api.qcloud.com', port=443, region='gz')
        i_ctx = TecentContext(KEY_ID, KEY_SECRET,
                              host='api.qcloud.com', port=443, region='gz')
        image = TecentImageSupport(cxt)
        instance = TecentInstanceSupport(i_ctx)
        instance.stop(id)
        ret = image.create_image(from_instance=id, name='testgquery1')
        print(ret)
        self.assertIsNotNone(ret)

    def test_list_regions(self):
        ctx = TecentContext(KEY_ID, KEY_SECRET,
                            host='api.qcloud.com', port=443, region='gz')
        dc = TecentDCSupport(ctx)
        dcs = dc.list_regions()
        self.assertIsNotNone(dcs)
        print(dcs)

    def test_create_instance(self):
        cxt = TecentContext(KEY_ID, KEY_SECRET, host='api.qcloud.com', port=443, region='gz')
        instance = TecentInstanceSupport(cxt)
        # mem,cpu,storageSize,period
        rsp = instance.launch(image='1470', mem=4, cpu=2, storageSize=100, period=1)
        self.assertIsNotNone(rsp)

    def test_remove_instance(self):
        cxt = TecentContext(KEY_ID, KEY_SECRET, host='api.qcloud.com', port=443, region='gz')
        instance = TecentInstanceSupport(cxt)
        instance.remove('qcvmfa85f0497c33536dc641eaed5c4e3818')




