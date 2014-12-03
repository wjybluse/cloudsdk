# -*- coding: utf-8 -*-
__author__ = 'wan'
# ScalingRule manager all rule access
# 1.provider some basic method to use rule
#2.communication with database

class ScalingRule():
    def __init__(self):
        pass

    def register(self, name, **kwargs):
        """
        :param name: rule name,unique
        :param kwargs: condition of rule
        :return:nothing,if error,raise exception
        """
        pass

    def deregister(self, name):
        """
        :param name:deregister rule,name is unique
        :return:if can not deregister ,raise exception
        """
        pass

    def active(self, name):
        """
        :param name: active rule,default is active,you can change to unactive when not in using
        :return:nothing if no exception
        """
        pass

    def unactive(self, name):
        """
        :param name: unactive rule name
        :return:
        """
        pass

    def is_scaling(self, name):
        """
        :param name: check rule is in using or not
        :return:
        """
        pass

    def query_all_rule(self):
        """
        :return:return all rule has created
        """
        pass

    def query_rule(self, **kwargs):
        """
        :param kwargs: query rule by condition
        :return:
        """
        pass