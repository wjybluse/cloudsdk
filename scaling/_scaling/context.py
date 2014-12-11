__author__ = 'wan'
from _toolbox.logger import log


class ScaleContext():
    def __init__(self, name='ali', operation_obj='instance', image=None, instance=None,
                 flavor=None,
                 region=None,
                 bandwidth=None,
                 snapshot=None, size=None, **kwargs):
        """
        :param instance: id of instance
        :param name :the name of cloud
        :param operation_obj:volume or instance
        :param image:image id
        :param flavor: flavor like small.tiny1
        :param region: region
        :param bandwidth:400
        :param snapshot: snapshot of volume
        :param size: size of volume
        :param kwargs: other args like security group
        :param action:_scaling in or _scaling out
        :return:
        """
        self.operation_obj = operation_obj
        self.image = image
        self.name = name
        self.instance = instance
        self.flavor = flavor
        self.region = region
        self.bandwidth = bandwidth
        self.snapshot = snapshot
        self.size = size
        self.kwargs = kwargs

    # 1.if kwargs is None return None
    # 2.if context contains key,set value
    # 3.if context does not contains key,update context.kwargs
    # 4.return context value
    @staticmethod
    @log
    def covert_to_context(**kwargs):
        """
        :param kwargs: context params
        :return:
        """
        if kwargs is None:
            return None
        context = ScaleContext('', '')
        for key, val in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, val)
            else:
                context.kwargs[key] = val
        return context
