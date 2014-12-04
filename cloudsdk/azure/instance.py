# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.instance import InstanceSupport
from _common import BaseSupport
from azure.servicemanagement import *


class AzureInstanceSupport(InstanceSupport):
    def __init__(self, ctx):
        self.azure = BaseSupport.instance(ctx.access_key).service_management
        self.ctx = ctx

    def launch(self, image=None, flavor=None, hostname=None, bandwidth=None, **kwargs):
        """
        azure create vm is so complex,fuck
        :param image: image name
        :param flavor: role size
        :param hostname:support host name
        :param bandwidth:nothing
        :param kwargs:media_link,username,password,support change the image password?
        :return:the instance object
        """
        name = self.ctx.service_name
        self.azure.create_hosted_service(service_name=name,
                                         label=name,
                                         location=self.ctx.region)
        linux_config = LinuxConfigurationSet(hostname, kwargs['username'], kwargs['password'], True)
        os_hd = OSVirtualHardDisk(image, kwargs['media_link'])
        return self.azure.create_virtual_machine_deployment(service_name=name,
                                                            deployment_name=name,
                                                            deployment_slot='production', label=name,
                                                            role_name=name,
                                                            system_config=linux_config,
                                                            os_virtual_hard_disk=os_hd,
                                                            role_size=flavor)


    def start(self, instance):
        self.azure.start_role(instance, instance, instance)

    def stop(self, instance, force=False):
        self.azure.shutdown_role(instance, instance, instance)

    def list_instances(self):
        return self.azure.list_role_sizes()

    def remove_instance(self, instance):
        """
        deploy name?service name is what
        :param instance:
        :return:
        """
        self.azure.delete_deployment(service_name=instance,
                                     deployment_name=instance)