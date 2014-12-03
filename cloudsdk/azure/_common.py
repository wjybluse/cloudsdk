# -*- coding: utf-8 -*-
__author__ = 'wan'
import os
from azure.servicemanagement import ServiceManagementService


class BaseSupport():
    cls = None

    def __init__(self, access_key):
        """
        :param access_key: subscription_id
        #certificate_path the
        :return: cons
        """
        self.certificate_path = os.path.join('../conf/', 'mycert.cer')
        self.sms = ServiceManagementService(access_key)

    @property
    def service_management(self):
        return self.sms

    @classmethod
    def instance(cls, access_key):
        if cls.cls is None:
            cls.cls = cls()
        return cls.cls