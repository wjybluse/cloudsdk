# -*- coding: utf-8 -*-
__author__ = 'wan'
import os

from _toolbox.utils import RouteError


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