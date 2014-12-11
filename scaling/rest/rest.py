# -*- coding: utf-8 -*-
__author__ = 'wan'
import base64
import json
import abc

import yaml
from gevent.pywsgi import *

from scaling.orm.mongo import DBServer
from . import ConfigUtil
from _toolbox.utils import RestError, RouteError
from _toolbox.logger import LogFactory
from _toolbox.utils import Utils


HANDLERS = dict(get="query", head="query", link="query", post="add", put="update", patch="update", delete="delete")
CODE_MSG = {404: "Not Found", 400: "Bad Request", 401: "Unauthorized", 500: "Internal Server Error",
            501: "Not Implemented", 503: "Service Unavailable", 200: "OK", 204: "No Content"}

logger = LogFactory.logger(__name__)


class RestServer():
    def __init__(self, port=80, **ssl_args):
        """
        :type ssl_args: hash,the key store file and trust store
        """
        self.server = WSGIServer(("", port), application=self._dispatch, **ssl_args)
        self.route = Router()

    def start(self):
        """
        start the service
        :return:

        """
        logger.info("start the server.......")
        self.server.serve_forever()

    def close(self):
        """
        close the service
        :return:
        """
        self.server.close()

    def _dispatch(self, env, start_response):
        logger.info("Receive message", "invoke dispatch")
        method = env['REQUEST_METHOD']
        if not auth(env):
            start_response(status(401, CODE_MSG[401]), headers())
            return response(error_message("Authorization failed"))
        data = None
        if method.lower() not in ["patch", "post", "put"]:
            # if not method in list ,skip
            logger.info("The method is", method, "skip validate")
        else:
            content_type = env['CONTENT_TYPE']
            if "application/json" not in content_type:
                start_response(
                    status(501, CODE_MSG[501]),
                    headers())
                return response(error_message("The type can not be supported"))
            content_len = env['CONTENT_LENGTH']
            data = env['wsgi.input'].read(content_len).replace("\n\t", "\n")
        try:
            value = self.handle_route(env)(data)
            logger.info("The type of data", value)
        except Exception, e:
            logger.error("Send message error", e)
            code = getattr(e, 'code', 400)
            start_response(
                status(code, CODE_MSG[code]),
                headers())
            return response(error_message(e.message))
        if value is None:
            logger.info("return message is empty")
            start_response(status(200, CODE_MSG[200]), headers())
            return response(ok_message("OK"))
        logger.info("return message", value)
        start_response(status(200, CODE_MSG[200]), headers())
        return response(value)

    def handle_route(self, env):
        url = env['PATH_INFO']
        if url.endswith("/"):
            url = url[:-1]
        method = env['REQUEST_METHOD']
        q_string = env['QUERY_STRING']
        try:
            dic, arr, name, conditions = self.route.handle(method.lower(), url, q_string)
            handler = Handler.create_handler(name, dic, arr)
            return lambda data: handler.invoke(data, **conditions)
        except Exception, e:
            logger.error("The error message ", e)
            if isinstance(e, RouteError):
                logger.info("The error message ", e)
                raise RestError(e.code, e.message)
            raise RestError(500, e.message)


def auth(env):
    try:
        logger.warn("The header info", env)
        basic = env["HTTP_AUTHORIZATION"]
        logger.debug("Find the auth info", basic)
    except KeyError, e:
        logger.error("Authorization failed", e)
        return False
    if basic is None or len(basic) <= 0:
        return False
    user, password = base64.decodestring(basic.split("Basic ")[1] + "\n").split(":")
    # read from config file
    s_user, pwd = ConfigUtil.auth_config()
    return s_user == user and pwd.strip() == password.strip()


def headers():
    return [('Content-type', 'application/json'),
            ("Server", "Ever homes")]


def status(state, message):
    return "{0} {1}".format(state, message)


def error_message(message):
    return {"error": message}


def ok_message(message):
    return {"message": message}


def response(message=None):
    if not message:
        message = dict()
    logger.info("Response is :", message)
    return [json.dumps(message)]


class Router():
    def __init__(self):
        self.cache = None
        self.init()

    def handle(self, method, url, q_string):
        logger.info("method is ", method, "url is", url, "query string is", q_string)
        if self.cache.__contains__(method):
            queues = self.cache[method]
            return Router.match(url, q_string, queues)
        raise RouteError(501, "The method is not supported")

    def init(self):
        self.cache = ConfigUtil.route_build()
        logger.debug('find the route', self.cache)

    @staticmethod
    def match(url, q_string, queues):
        """
        :param url: real url
        :param q_string: query_string
        :param queues: tpl queue
        :return:dic or url params,list of url params,deal handler,query conditions
        """
        conditions = _parser(q_string)
        prefix_arr = url.split("/")
        for tpl in queues:
            if len(tpl) == 0:
                continue
            tpl_arr = tpl[0].split("/")
            if len(prefix_arr) != len(tpl_arr):
                continue
            # return the dict mode or arr mode of params
            dic, arr = Router.find_options(tpl_arr, prefix_arr)
            if dic is None and arr is None:
                continue
            handler = tpl[1]
            logger.info("Find the router for the url", url)
            return dic, arr, handler, conditions
        logger.error('Can not find the template', 'url=', url)
        raise RouteError(404, 'The route can not find')

    # 因为路由不是很复杂，所以现在基本上就是支持简单的匹配即可，不需要去使用开源的路由规则
    @staticmethod
    def find_options(tpl_arr, prefix_arr):
        """
        :param tpl_arr: tpl split by slash to arr
        :param prefix_arr: prefix of real url
        :return:dict mode and dict mode of tpl
        """
        arr_index = []
        for index in range(0, len(tpl_arr)):
            if tpl_arr[index].startswith(":"):
                arr_index.append(index)
                continue
            if not tpl_arr[index].__eq__(prefix_arr[index]):
                return None, None
        if len(arr_index) <= 0:
            return {}, []
        dic_options = {}
        arr_options = []
        for value in arr_index:
            val = prefix_arr[value]
            arr_options.append(val)
            dic_options[tpl_arr[value].replace(":", "")] = val
        return dic_options, arr_options


def _parser(q_string):
    """
    :param q_string: string like key=value&key1=value2
    :return:dict of key mapping to value
    """
    if Utils.is_empty(q_string):
        return {}
    conditions = {}
    for condition in q_string.split("&"):
        arr = condition.split("=")
        for index in range(0, 2, len(arr)):
            conditions[arr[index]] = arr[index + 1]
        logger.debug("The query string is", conditions)
    return conditions


class Handler():
    def __init__(self, name, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        if name not in ["io", "redis", "mysql", "ram", "http", "connect", 'rule', 'alarm']:
            # 如果是自定义的，自己处理
            self.server = None
        else:
            self.server = DBServer('everhomes_{0}'.format(name), 'tasks')

    @abc.abstractmethod
    def invoke(self, data=None, **conditions):
        raise NotImplementedError("The method is not Implemented")

    def close(self):
        self.server.close()

    @staticmethod
    def create_handler(name, dic, arr):
        if len(name.split('.')) > 2:
            # if is extension handler, do yourself
            module, class_form = name.split('.')[:-1], name.split('.')[-1]
            module = __import__('.'.join(module), fromlist=[class_form])
            return getattr(module, class_form)('', *arr, **dic)
        module = __import__(Handler.__module__, fromlist=[name])
        return getattr(module, name)(arr[0])

    @staticmethod
    def unknown_handler(method, name, params):
        return ExtensionHandler(method, name, params)


"""
_toolbox handler to deal with system request
if you want to extension,please use extension interface
or define your own handler
"""


class QueryHandler(Handler):
    def invoke(self, data=None, **conditions):
        logger.info("Invoke method,begin to transfer", self.__class__)
        return self.server.query(**conditions)


class AddHandler(Handler):
    def invoke(self, data=None, **conditions):
        logger.info("Invoke method,begin to transfer", self.__class__)
        self.server.insert(yaml.load(data))


class UpdateHandler(Handler):
    def invoke(self, data=None, **conditions):
        logger.info("Invoke method,begin to transfer", self.__class__, "data=", data, "condition=", conditions)
        # for update ,we should care update key,
        # route like this: /openstack/action/:nova/update/:id,
        # we will key the id key,and default is id
        # if extension ,what you can do
        if len(self.args) != 2:
            raise RestError('400', 'update does not supported')
        self.server.update(yaml.load(data), id=self.args[1], **conditions)


class DeleteHandler(Handler):
    def invoke(self, data=None, **conditions):
        logger.info("Invoke method,begin to transfer", self.__class__)
        self.server.delete(**conditions)


# 对于没办法识别的消息现在的处理直接报错
class ExtensionHandler(Handler):
    def invoke(self, data=None, **conditions):
        raise RouteError(400, "The bad request")


class CountHandler(Handler):
    def invoke(self, data=None, **conditions):
        if len(self.args) == 2:
            return self.server.count(id=self.args[1])
        return self.server.count(**conditions)
