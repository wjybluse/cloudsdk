# -*- coding: utf-8 -*-
__author__ = 'wan'
import abc
# provide auth context
# kwargs contains username,password,endpoint and so on
# can get value :
# auth=AuthContext(user='username',password='password')
# auth.user


class AuthContext():
    def __init__(self, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.host = host
        self.port = port
        if kwargs is None:
            raise ValueError("auth context can not be empty")
        for key, val in kwargs.items():
            setattr(self, str(key), str(val))

    @abc.abstractmethod
    def get_context(self):
        """
        :return:return function of sign,use like get_context()(action="DescribeInstance",regionId='region')
        :return the url encoding
        """
        pass

    @abc.abstractmethod
    def get_headers(self):
        """
        :return:the dict of headers
        """
        pass