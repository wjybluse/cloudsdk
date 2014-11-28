# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
from cloudsdk.rest.request import Request


class SecurityGroupSupport():
    def __init__(self, ctx):
        self.ctx = ctx
        self.request = Request(ctx)

    @abc.abstractmethod
    def create_security_group(self, name=None, description=None, **kwargs):
        pass

    @abc.abstractmethod
    def list_security_group(self):
        pass