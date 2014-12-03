# -*- coding: utf-8 -*-
__author__ = 'wan'
import unittest
from cloudsdk.aws.image import AWSImageSupport
from cloudsdk.aws.instance import AWSInstanceSupport
from cloudsdk.aws.context import AWSContext
from cloudsdk.aws.datacenter import AWSDCSupport
from cloudsdk.aws.security import AWSSecurityGroupSupport
from cloudsdk.aws.volume import AWSVolumeSupport

AWS_KEY = ''
SECRET_KEY = ''


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

    def test_create_instance(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY, host='ec2.amazonaws.com',
                         port=443, region='us-east-1')

        instance = AWSInstanceSupport(ctx)
        instance_id = instance.launch(image='ami-aeb532c6', flavor='t2.micro', KeyName='free')
        print(instance_id)
        self.assertIsNotNone(instance_id)

    def test_list_sg(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY, host='ec2.amazonaws.com',
                         port=443, region='us-east-1')

        sg = AWSSecurityGroupSupport(ctx)
        ret = sg.list_security_group()
        print(ret)
        self.assertIsNotNone(ret)

    def test_create_sg(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY, host='ec2.amazonaws.com',
                         port=443, region='us-east-1')

        sg = AWSSecurityGroupSupport(ctx)
        ret = sg.create_security_group(name='wan', description="testnime")
        print(ret)
        self.assertIsNotNone(ret)

    def test_list_volumes(self):
        ctx = AWSContext(AWS_KEY, SECRET_KEY, host='ec2.amazonaws.com',
                         port=443, region='us-east-1')
        volume = AWSVolumeSupport(ctx)
        ret = volume.list_volume()
        print(ret)
        self.assertIsNotNone(ret)
