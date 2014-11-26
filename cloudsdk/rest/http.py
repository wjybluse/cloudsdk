# -*- coding: utf-8 -*-
__author__ = 'wan'
import json
from httplib import HTTPConnection, HTTPSConnection
from cloudsdk.tool.logger import LogFactory

logger = LogFactory.logger(__name__)


class HTTPSupport():
    def __init__(self, host="localhost", port=80):
        self.host = host
        self.port = port
        self.headers = dict()
        self._client = None

    @staticmethod
    def _response(msg):
        return json.dumps(msg)

    def send(self, method="get", url="/", body=None, headers={}, callback=None):
        """
        :param method: support[get,post,put,patch,delete]
        :param url: /everhomes/push/data
        :param body: dict or object,current support dict
        :param headers: dict
        :param callback: callback deal with data
        :return:
        """
        logger.info("Invoke send method", "method=", method, "url=", url, "body=", body, "headers=", headers)
        self._client.request(method, url, headers=headers)
        rsp = self._client.getresponse()

        if rsp is None:
            raise IOError("can not receive message")
        message = rsp.read()
        status = rsp.status
        logger.info("Receive response message", rsp, "status", status, "message", message)
        if callback is not None:
            return callback(status, message)
        logger.info("Receive response message", "status=", status)
        if status < 200 or status > 204:
            return {"status": status, "message": message}
        logger.info("body=", message)
        return HTTPSupport._response(message)

    def close(self):
        if self._client is not None:
            self._client.close()


class HTTPClient(HTTPSupport):
    def __init__(self, host="localhost", port=80):
        """
        :param host: str,host name
        :param port: int ,server port
        """
        HTTPSupport.__init__(self, host=host, port=port)
        self._client = HTTPConnection(self.host, self.port)


class HTTPSClient(HTTPSupport):
    def __init__(self, host="localhost", port=443):
        """
        :param host: str,host name
        :param port: int ,server port
        """
        logger.info("Invoke https client")
        HTTPSupport.__init__(self, host=host, port=port)
        if str(self.port).__eq__('443'):
            self._client = HTTPSConnection(self.host)
        else:
            self._client = HTTPSConnection(self.host, port=self.port)
