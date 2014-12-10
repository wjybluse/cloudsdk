__author__ = 'wan'
from cloudsdk.api.autoscale import AutoScaling
from _base import validate_rsp
from _toolbox.logger import log
# ali support ess

class AliAutoScaling(AutoScaling):
    def __init__(self, context):
        context.host = 'ess.aliyuncs.com'
        setattr(context, 'version', '2014-08-28')
        AutoScaling.__init__(self, context)

    @log
    def create_scaling_group(self, name, max, min, **kwargs):
        rsp = self.request.invoke(Action='CreateScalingGroup', MaxSize=max, MinSize=min, ScalingGroupName=name,
                                  **kwargs)
        validate_rsp(rsp)
        rsp = eval(rsp)
        return eval(rsp)['ScalingGroupId']

    @log
    def list_scaling_groups(self):
        rsp = self.request.invoke(Action='DescribeScalingGroups')
        validate_rsp(rsp)
        rsp = eval(rsp)
        if 'ScalingGroups' not in eval(rsp):
            return None
        groups = []
        for item in eval(rsp)['ScalingGroups']['ScalingGroup']:
            groups.append(item)
        return groups

    @log
    def active_scaling_group(self, group):
        rsp = self.request.invoke(Action='EnableScalingGroup', ScalingGroupId=group)
        validate_rsp(rsp)

    @log
    def unactive_scaling_group(self, group):
        rsp = self.request.invoke(Action='DisableScalingGroup', ScalingGroupId=group)
        validate_rsp(rsp)

    @log    
    def remove_scaling_group(self, group):
        rsp = self.request.invoke(Action='DeleteScalingGroup', ScalingGroupId=group)
        validate_rsp(rsp)
