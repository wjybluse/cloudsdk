# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from cloudsdk.aws.image import AWSImageSupport
from cloudsdk.aws.instance import AWSInstanceSupport
from cloudsdk.aws.context import AWSContext
from cloudsdk.aws.datacenter import AWSDCSupport

AWS_KEY = 'your key'
SECRET_KEY = 'your secret'


class TestAWSSDK(unittest.TestCase):
    def test_query_images(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY, host='ec2.amazonaws.com',
                         port=443, region='us-east-1')
        image = AWSImageSupport(ctx)
        ret = image.list_images()
        self.assertIsNotNone(ret)
        print(ret)

    def test_query_instance(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY, host='ec2.amazonaws.com',
                         port=443, region='us-east-1')

        instance = AWSInstanceSupport(ctx)
        instances = instance.list_instances()
        print(instances)
        self.assertIsNotNone(instances)

    def test_create_image(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY,
                         host='ec2.amazonaws.com',
                         port=443, region='us-east-1')
        image = AWSImageSupport(ctx)
        rsp = image.create_image(from_instance='i-180872f9', name='wan123')
        print(rsp)
        self.assertIsNotNone(rsp)

    def test_list_region(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY,
                         host='ec2.amazonaws.com',
                         port=443, region='us-east-1')
        dc = AWSDCSupport(ctx)
        rsp = dc.list_regions()
        print(rsp)
        self.assertIsNotNone(rsp)

    def test_list_zones(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY,
                         host='ec2.amazonaws.com',
                         port=443, region='us-east-1')
        dc = AWSDCSupport(ctx)
        rsp = dc.list_zones()
        print(rsp)
        self.assertIsNotNone(rsp)
