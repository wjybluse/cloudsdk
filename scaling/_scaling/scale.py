# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
import random
import string

from _toolbox.utils import *
from _toolbox.logger import log
from _toolbox.logger import LogFactory


logger = LogFactory.logger(__name__)
CLOUD_INFO = dict(ali=['ecs.aliyuncs.com', 443, 'xx', 'xx', 'cn-shenzhen'],
                  tecent=['api.qcloud.com', 443, 'xx', 'xx', 'gz'],
                  aws=['ec2.amazonaws.com', 443, 'xx', 'xx',
                       'us-east-1'],
                  azure=['', 443, '', '', ''])


class ScaleHandler():
    def __init__(self):
        pass

    @abc.abstractmethod
    def scale_in(self):
        """
        :return:id of device
        """
        pass

    @abc.abstractmethod
    def scale_out(self):
        """
        :return: id of device
        """
        pass

    @abc.abstractmethod
    def _list(self, **conditions):
        pass

    @abc.abstractmethod
    def _details(self, **conditions):
        pass


def get_region(context, cloud):
    return context.region or CLOUD_INFO[cloud][4]


class ScaleProxy(ScaleHandler):
    def __init__(self, context):
        ScaleHandler.__init__(self)
        name = context.name
        module_name = 'cloudsdk.{0}.provider'.format(name)  # package name like cloudsdk.ali.provider
        class_name = '{0}CloudProvider'.format(name.capitalize())  # name like AliProvider,AwsProvider and so on
        service = __import__(module_name, fromlist=[class_name])
        _provider = getattr(service, class_name).instance(CLOUD_INFO[name][2], CLOUD_INFO[name][3],
                                                          region=get_region(context, name), host=CLOUD_INFO[name][0],
                                                          port=CLOUD_INFO[name][1],
                                                          **context.kwargs)
        _handler = '{0}Handler'.format(context.operation_obj.capitalize())
        module = __import__(ScaleProxy.__module__, fromlist=[_handler])
        self.handler = getattr(module, _handler)(_provider, context)

    @log
    def scale_in(self):
        return self.handler.scale_in()

    @log
    def scale_out(self):
        return self.handler.scale_out()

    def _list(self, **conditions):
        return self.handler._list(**conditions)

    def _details(self, **conditions):
        return self.handler._details(**conditions)


class VolumeHandler(ScaleHandler):
    def __init__(self, provider, context):
        """
        :param provider: provider of cloud
        :param context:information
        :return:
        """
        ScaleHandler.__init__(self)
        self.context = context
        self.provider = provider

    @log
    def scale_in(self):
        """
        first detach volume,and the remove
        :return:
        """
        try:
            if self.context.instance is not None:
                self.provider.volume_support().detach_volume(instance=self.context.instance, volume=self.context.volume)
            self.provider.volume_support().remove_volume(volume=self.context.volume)
        except Exception, e:
            logger.error("remove volume failed", e)
            raise RestError(500, e.message)

    @log
    def scale_out(self):
        """
        create and attach
        :return:
        """
        try:
            volume_id = self.provider.volume_support().create_volume(snapshot=self.context.snapshot,
                                                                     size=self.context.size,
                                                                     **self.context.kwargs)
            if self.context.instance is not None:
                self.provider.volume_support().attach_volume(instance=self.context.instance, volume=volume_id)
            return dict(volume=volume_id)
        except Exception, e:
            logger.error("create or attach failed volume failed", e)
            raise RestError(500, e.message)

    def _list(self, **conditions):
        return dict(volumes=self.provider.volume_support().list_volume())

    def _details(self, **conditions):
        if 'id' not in conditions:
            logger.error('volume id can not be empty', conditions)
            raise RestError(400, 'volume id can not be empty')
        return self.provider.volume_support().query_volume_details(conditions['id'])


class InstanceHandler(ScaleHandler):
    def __init__(self, provider, context):
        """
        :param provider: provider of cloud
        :param context:information
        :return:
        """
        ScaleHandler.__init__(self)
        self.context = context
        self.provider = provider

    @log
    def scale_in(self):
        """
        remove resource
        :return:
        """
        try:
            self.provider.instance_support().remove_instance(instance=self.context.instance)
        except Exception, e:
            logger.error("remove instance failed", e)
            raise RestError(500, e.message)

    @log
    def scale_out(self):
        """
        create vm
        """
        # if ali cloud,should provider SecurityGroupId
        security = self.get_security_group()
        try:
            if security is None:
                instance = self.provider.instance_support().launch(image=self.context.image,
                                                                   bandwidth=self.context.bandwidth,
                                                                   flavor=self.context.flavor,
                                                                   **self.context.kwargs)
                return dict(instance=instance)
            instance = self.provider.instance_support().launch(image=self.context.image,
                                                               bandwidth=self.context.bandwidth,
                                                               SecurityGroupId=security, flavor=self.context.flavor,
                                                               **self.context.kwargs)
            return dict(instance=instance)
        except Exception, e:
            logger.error("launch vm failed", e)
            raise RestError(500, e.message)

    def _list(self, **conditions):
        return dict(instances=self.provider.instance_support().list_instances())

    def _details(self, **conditions):
        if 'id' not in conditions:
            logger.error('instance id can not be empty', conditions)
            raise RestError(400, 'instance id can not be empty')
        return self.provider.instance_support().query_instance_details(conditions['id'])

    def get_security_group(self):
        # need create?
        # default get index 0,the system default  security group
        try:
            ret = self.provider.security_support().list_security_group()
            if ret is None or len(ret) <= 0:
                return None
            return ret[0]
        except NotImplementedError, e:
            logger.error("the method not implement", e)
            return None


class ImageHandler(ScaleHandler):
    def __init__(self, provider, context):
        ScaleHandler.__init__(self)
        self.context = context
        self.provider = provider

    def scale_in(self):
        try:
            self.provider.image_support().remove_image(self.context.image)
        except Exception, e:
            logger.error("remove image failed", e)
            raise RestError(500, e.message)


    def scale_out(self):
        # create image name if not given the name
        image_name = (lambda: self.context.kwargs[
            'imageName'] if 'imageName' in self.context.kwargs else self.context.name + '_' + ''.join(
            random.choice(string.lowercase) for i in range(5)))()
        try:
            if self.context.snapshot is None:
                image = self.provider.image_support().create_image(from_instance=self.context.instance, name=image_name)
                return dict(image=image)
            image = self.provider.image_support().create_image(from_snapshot=self.context.snapshot, name=image_name)
            return dict(image=image)
        except Exception, e:
            logger.error("create image failed", e)
            raise RestError(500, e.message)

    def _list(self, **conditions):
        return dict(images=self.provider.image_support().list_images())

    def _details(self, **conditions):
        if 'id' not in conditions:
            logger.error('image id can not be empty', conditions)
            raise RestError(400, 'image id can not be empty')
        return self.provider.image_support().query_image_details(conditions['id'])
