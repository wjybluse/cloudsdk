# -*- coding: utf-8 -*-
# 定时检查任务是否有到达指定的条件，到达之后直接触发伸缩
# 没有的话继续检查，检查周期为自定义
# rule object
# {last_scaling_time,cool_down,is_scaling,active,name,condition}
# :last_scaling_time,default is rule create time,update when scaling
# :cool_down,cool down time,if >0 ,can do nothing for rule
# :is_scaling,
# :active,is active
# :name rule name
# :condition,scale rule condition like http request cpu >90%
__author__ = 'wan'


class Scheduler():
    def __init__(self, db, scale):
        """
        :param db: database
        :param scale: scale controller
        :return:
        """
        self.db = db
        self.scale = scale

    def start(self):
        pass

    def compare(self):
        pass