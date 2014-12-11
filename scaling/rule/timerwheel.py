# -*- coding: utf-8 -*-
__author__ = 'wan'
from greenclock import Scheduler, every_second

import rule
from scaling.orm import DefaultConditionUtil
from _toolbox.logger import LogFactory


logger = LogFactory.logger(__name__)
"""
check the health of service
if service is health,do nothing
else send alarm,the condition is rule
"""

"""
1.定时任务去匹配规则，如果都满足，则报警或者是恢复报警
2.发邮件通知管理员进行处理
3.处理的方式就是伸缩
"""


class TimerWheel():
    def __init__(self):
        self.scheduler = Scheduler()

    def add_task(self, name, task, tick=20):
        logger.debug("add task", task, 'name', name, 'tick', tick)
        self.scheduler.schedule(name, every_second(tick), task)

    def start(self):
        logger.debug('run task for ever')
        self.add_task('default task', TimerWheel._pattern_rule)
        self.scheduler.run_forever()

    @staticmethod
    def _pattern_rule():
        rules = _query_rules()
        if rules is None or len(rules) <= 0:
            logger.info('rules is empty')
            return
        for s_rule in rules:
            if not isinstance(s_rule, dict):
                logger.info('The rule is invalid', s_rule)
                continue
            need_alarm = True
            for obj, condition in s_rule.items():
                # if not list ,skip and continue
                if not isinstance(condition, list):
                    continue
                expression = _get_expression(condition)
                if len(expression) <= 0:
                    continue
                if not validate(obj, expression):
                    need_alarm = False
                    break
            if need_alarm:
                _send_alarm(s_rule)
                _send_email(s_rule)

    def stop(self):
        self.scheduler.stop()


def _get_expression(conditions):
    dtc = DefaultConditionUtil(*conditions)
    return dtc.get_complex_expression()


def _send_email(s_rule):
    # TODO
    pass


def _send_alarm(s_rule):
    rule.Rule.send_alarm(dict(type='Important', belong_to=s_rule['_name'], reason='overload', key=s_rule))


def _query_rules():
    rules = rule.Rule.find_all()
    return rules


def validate(key, condition):
    return rule.Rule.validate(key, condition)