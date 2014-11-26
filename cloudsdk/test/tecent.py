__author__ = 'wan'
import unittest
from cloudsdk.tecent.instance import TecentInstanceSupport
from cloudsdk.tecent.cotext import TecentContext
from cloudsdk.tecent.image import TecentImageSupport

KEY_ID = 'your key'
KEY_SECRET = 'your secret'


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
        ret = image.create_image(from_instance=id, name='wan3')
        print(ret)
        self.assertIsNotNone(ret)



