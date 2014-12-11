# -*- coding: utf-8 -*-
__author__ = 'wan'
import yaml

from _toolbox.utils import ScaleError
from _toolbox.utils import RestError
from scaling.rest.rest import Handler
from scaling._scaling.context import ScaleContext
from scaling._scaling.scale import ScaleProxy
from scaling.rule.manager import RuleManager
from _toolbox.logger import LogFactory
from _toolbox.logger import log


logger = LogFactory.logger(__file__)


class ExtHandler(Handler):
    def invoke(self, data=None, **conditions):
        return {'hello': 'world'}


"""
rule handler support add remove update and get rule data
1.provider standard rest api
2.relation to the db
3.example:
    add:
        method:POST
        header:application/json
        url:http://<host:port>/everhomes/metric/rule/action/add
        body:
            {
                "_name":"test_rule",
                "cpu":["usage>80%",'virtual>9000'],
                "ram":["usage>90%"],
                "io":["write>3000/s","read>5000/s"],
                "mysql":["client>3000","read>5000/s"],
                "redis":["client>4000"]
            }
    delete:
        method:DELETE
        url:http://<host:port>/everhomes/metric/rule/action/remove/test_rule
    get:
        method:GET
        url:http://<host:port>/everhomes/metric/rule/action/list?name=test_rule
    update:
        method:PATCH
        header:application/json
        url:http://<host:port>/everhomes/metric/rule/action/update/test_rule
        body:
            {
                "_name":"test_rule",
                "cpu":["usage>85%",'virtual>9000'],
                "ram":["usage>90%"],
                "io":["write>3000/s","read>5000/s"],
                "mysql":["client>3000","read>5000/s"],
                "redis":["client>4000"]
            }
"""


class RuleHandler(Handler):
    @log
    def invoke(self, data=None, **conditions):
        action = self.args[0]
        if action == 'add':
            _register(data)
            return
        if action == 'remove':
            if len(self.args) != 2:
                raise TypeError('Does not support this url')
            _deregister(self.args[1])
            return
        if action == 'update':
            if len(self.args) != 2:
                raise TypeError('Does not support this url')
            _update(self.args[1], data)
            return
        return _query(**conditions)


def _update(cd, data):
    pass


def _register(data):
    data = eval(data)
    if '_name' not in data:
        logger.error('data is invalid', data)
        raise ValueError('can not support the rule')
    rule = RuleManager()
    rule.register(data['_name'], **data)


def _deregister(name):
    rule = RuleManager()
    rule.deregister(name)


def _query(**conditions):
    rule = RuleManager()
    return rule.query(**conditions)


"""
scale handler is the core of this package
can support volume,instance _scaling
1.current support post and delete method
2.post like
    Header:Content-Type:application/json
    Method:POST
    Url:/everhomes/scale/:opbj/action/:action
    Example:
        http://<host>:port/everhomes/scale/volume/action/scale_out
        Body:
        {
            "image":"m-94u39dy7r",
            "flavor":"ecs.t1.xsmall",
            "bandwidth":40,
            "name":"ali",
            "xxxx":"xxxx"
        }

2.delete like
Example:
       delete http://<host>:port/everhomes/scale/volume/action/scale_in?instance=i.237vdfs&volume=disk_323dadsa

"""


class ScaleHandler(Handler):
    """
    scale handler for manual _scaling
    the body should contains the message:
    1.for virtual machine(scale out):
        :param image id,region id,bandwidth,flavor and hostname
    2.for virtual machine(scale in)
        :param virtual machine id,if attach some volume ,should include volume ids or scale in volume before
    3.for volume (scale out)
        :param snapshot id or size,name,vm id if need attach to vm
    4.for volume (scale in)
        :param vm id if attach in vm,volume id
    """

    @log
    def invoke(self, data=None, **conditions):
        """
        :param data: body object for scale out
        :param conditions:volume id of instance id for scale in
        :return:
        """
        if len(self.args) < 2:
            logger.error('can not support scale type')
            raise ValueError("can not support scale type")
        operate_obj, action = self.args
        validate_message(action, data, **conditions)
        # update data is data is None
        data = yaml.load(data) or {}
        data.update(**conditions)
        context = ScaleContext.covert_to_context(operation_obj=operate_obj, **data)
        scale = ScaleProxy(context)
        # invoke the proxy scale_in or scale_out method
        if not hasattr(scale, action):
            raise RestError(501, 'UnSupport method ' + action)
        return getattr(scale, action)()


@log
def validate_message(action, data, **conditions):
    if action not in ['scale_out', 'scale_in']:
        logger.error('action can not supported.', 'Current support scale action is [scale_out,scale_in]')
        raise ScaleError(ScaleError.ACTION_NOT_SUPPORT, 'current support scale action is [scale_out,scale_in]')
    if action.__eq__('scale_out'):
        if data is None:
            logger.error('can not scale out', 'the body can not be empty')
            raise ScaleError(ScaleError.PARAMS_INVALID, 'body should given')
        return
    if action.__eq__('scale_in'):
        if conditions is None:
            logger.error('can not scale out', 'the condition can not be empty')
            raise ScaleError(ScaleError.PARAMS_INVALID, 'condition should given')


"""
query instance,volume,image details or snapshot
support url like:
/everhomes/:role/:action?instance=xxx&cloud=ali&region=cn-shenzhen
"""


class RoleDetailsHandler(Handler):
    def invoke(self, data=None, **conditions):
        if len(self.args) <= 0:
            logger.error("invalid request params", self.args)
            raise RestError(400, 'request params is invalid.')
        if conditions is None:
            logger.error('invalid conditions', conditions)
            raise RestError(400, 'request params is invalid.')
        if not 'cloud' in conditions:
            logger.error('invalid conditions', conditions)
            raise RestError(400, 'request params is invalid.')
        obj, action = self.args
        context = ScaleContext.covert_to_context(operation_obj=obj, name=conditions.pop('cloud'), **conditions)
        scale = ScaleProxy(context)
        if not hasattr(scale, '_{0}'.format(action)):
            raise RestError(501, 'UnSupport method ' + action)
        return getattr(scale, '_{0}'.format(action))(**conditions)
