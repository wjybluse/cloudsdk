# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.tool.logger import LogFactory
import base64

logger = LogFactory.logger(__name__)


class RestClient():
    def __init__(self, scheme="http", host="localhost", port=80):
        """
        :param scheme: str,support http or https
        :param host: str,the host name
        :param port: int,the port
        :return: init method
        """
        try:
            class_name = "{0}Client".format(scheme.upper())
            module = __import__("cloudsdk.rest.http", fromlist=[class_name])
            self.client = getattr(module, class_name)(host, port)
        except NotImplementedError, e:
            logger.info("The class not implement", self.__class__)
            raise NotImplementedError("The class not found " + e)
        add_dynamic_method(self, self._create)
        self.headers = {}

    def _msg(self, method="get", url=None, body=dict(), callback=None):
        """
        :param method: str,support ["get", "post", "delete", "patch", "put", "head", "unlink", "link"]
        :param url: str,simple url like /show/book/1
        :param body: hash,request body,current support json
        :param callback: function,'function(msg)'
        :return: the response with error msg
        """
        return self.client.send(method=method, url=url, body=body, headers=self.headers, callback=callback)

    def _create(self, m):
        """
        :param m: the method
        :return: return ref of build method
        """

        def build(url=None, body=None, callback=None):
            return self._msg(method=m, url=url, body=body, callback=callback)

        return build

    def add_header(self, key, value):
        self.headers[key] = value
        return self

    def remove_header(self, key):
        if self.headers.__contains__(key):
            self.headers.pop(key)
        return self

    def add_headers(self, **kwargs):
        self.headers.update(kwargs)
        return self

    def close(self):
        assert self.client is not None
        self.client.close()

    def default_headers(self):
        self.headers.update({"Content-Type": "application/json", "Accept": "application/json",
                             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
                             AppleWebKit/537.36 (KHTML, like Gecko) \
                             Chrome/38.0.2125.101 Safari/537.36"})
        return self

    def auth(self, user, password):
        self.headers["Authorization"] = "Basic " + base64.encodestring(user + ":" + password).replace("\n", "")
        return self


def add_dynamic_method(obj, ref):
    for m in ["get", "post", "delete", "patch", "put", "head", "unlink", "link"]:
        setattr(obj, m, ref(m.upper()))