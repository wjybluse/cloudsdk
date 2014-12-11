# -*- coding: utf-8 -*-
__author__ = 'wan'
import yaml
from . import Utils
from . import ScaleError
from scaling.rest.rest import Handler
from scaling.elastic.context import ScaleContext
from scaling.elastic.elastic import ScaleProxy
from scaling.rule.manager import RuleManager
from cloudsdk.tool.logger import LogFactory

logger = LogFactory.logger(__file__)


class ExtHandler(Handler):
    def invoke(self, data=None, **conditions):
        return {'hello': 'world'}


class RuleHandler(Handler):
    def invoke(self, data=None, **conditions):
        logger.warn('data=', data, 'condition=', conditions)
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
can support volume,instance scaling

"""


class ScaleHandler(Handler):
    """
    scale handler for manual scaling
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
        data = data or {}
        data.update(**conditions)
        context = ScaleContext.covert_to_context(**data)
        scale = ScaleProxy(context)
        # invoke the proxy scale_in or scale_out method
        return getattr(scale, action)()


def validate_message(action, data, **conditions):
    if action != 'scale_out' or action != 'scale_in':
        logger.error('action can not supported.', 'Current support scale action is [scale_out,scale_in]')
        raise ScaleError(ScaleError.ACTION_NOT_SUPPORT, 'current support scale action is [scale_out,scale_in]')
    if action == 'scale_out':
        if data is None:
            logger.error('can not scale out', 'the body can not be empty')
            raise ScaleError(ScaleError.PARAMS_INVALID, 'body should given')
        return
    if action == 'scale_in':
        if conditions is None:
            logger.error('can not scale out', 'the condition can not be empty')
            raise ScaleError(ScaleError.PARAMS_INVALID, 'condition should given')

