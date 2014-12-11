# -*- coding: utf-8 -*-
__author__ = 'wan'
import os


class Utils():
    def __init__(self):
        pass

    @staticmethod
    def close(obj):
        try:
            getattr(obj, 'close')()
        except AttributeError:
            pass

    @staticmethod
    def kill(obj):
        try:
            getattr(obj, 'kill')()
        except AttributeError:
            pass

    @staticmethod
    def is_empty(params):
        if params is None:
            return True
        if isinstance(params, dict) or isinstance(params, list) or isinstance(params, str):
            if len(params) <= 0:
                return True
        return False

    @staticmethod
    def contains(params, key):
        if params is None:
            return False
        if isinstance(params, str):
            return key in params
        if isinstance(params, dict) or isinstance(params, list):
            return params.__contains__(key)
        return False

    @staticmethod
    def is_expression(string):
        return '>' in string or '<' in string or '=' in string


class RouteError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__


class RestError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__


class ScaleError(Exception):
    ACTION_NOT_SUPPORT = 0x0001
    PARAMS_INVALID = 0x0002

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__


METHOD_SUPPORT = ['get', 'post', 'delete', 'patch', 'put', 'head', 'link', 'unlink']


class ConfigUtil():
    def __init__(self):
        pass

    @staticmethod
    def route_build():
        route = os.path.join(os.path.pardir, 'conf/route.cfg')
        controller = dict(get=[], post=[], delete=[], patch=[], put=[], head=[], link=[], unlink=[])
        with open(route, 'rb+') as f:
            current = controller['get']
            for line in f.readlines():
                if not line.startswith('['):
                    route = parser(line)
                    if route is None:
                        continue
                    current.append(route)
                    continue
                section = line.split('[')[1].split(']')[0].strip()
                if section not in METHOD_SUPPORT:
                    # 如果配置错误，就直接报错，先检查好了再用
                    raise RouteError('500', 'Method not supported')
                current = controller[section]
        return controller

    @staticmethod
    def auth_config():
        return 'admin', 'admin'


def parser(line):
    if 'controller' not in line:
        # skip may be is commet
        return None
    tpl, controller = line.split('controller')
    tpl, controller = tpl.strip(), controller.replace('=', '').strip()
    return [tpl, controller]


if __name__ == '__main__':
    cfg = ConfigUtil.route_build()
    print(cfg)