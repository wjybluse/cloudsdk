# -*- coding: utf-8 -*-
__author__ = 'wan'
import rule
import analytics as an
from greenclock import Scheduler, every_second
from cloudsdk.tool.logger import LogFactory
from scaling.rest import Utils

logger = LogFactory.logger(__file__)
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
        self.sched = Scheduler()

    def add_task(self, name, task, tick=2):
        logger.debug("add task", task, 'name', name, 'tick', tick)
        self.sched.schedule(name, every_second(tick), task)

    def start(self):
        logger.debug('run task for ever')
        self.sched.run_forever()

    def _query_rules(self):
        rules = rule.Rule.find_all()
        return rules

    def _pattern_rule(self):
        rules = self._query_rules()
        if rules is None or len(rules) <= 0:
            logger.info('rules is empty')
            return
        for s_rule in rules:
            if not isinstance(s_rule, dict):
                logger.info('The rule is invalid', s_rule)
                continue
            for key, val in s_rule:
                if not Utils.is_expression(val):
                    continue
                condition = an.SimpleAnalytics(val).analytics()
                # query from db find the result,how???
                ret = validate(key, condition)
                if not ret:
                    # if some condition not suit,skip
                    break
                logger.warn('send alarm', 'rule=', s_rule)
                self._send_alarm(s_rule)

    def _send_alarm(self, s_rule):
        rule.Rule.send_alarm(dict(type='Important', belong_to=s_rule['_name'], reason='overload', key=s_rule))

    def stop(self):
        self.sched.stop()


def validate(key, condition):
    return rule.Rule.validate(key, condition)


