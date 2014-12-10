# -*- coding: utf-8 -*-
__author__ = 'wan'
import time
import random
import hmac
import urllib
from hashlib import sha1
import base64

from cloudsdk.api.context import AuthContext
from _toolbox.logger import LogFactory
from _toolbox.utils import encode


logger = LogFactory.logger(__name__)
URL = '/v2/index.php'


class TecentContext(AuthContext):
    def get_context(self):
        logger.info("context", self.__dict__)
        params = dict(SecretId=self.access_key,
                      Timestamp=int(time.time()), Nonce=random.Random().randint(100000, 999999))
        if self.region is not None:
            params['Region'] = self.region
        logger.info("params", params)
        return sign(self.host, self.secret_key, **params)

    def get_headers(self):
        return {}


class URLParer():
    def __init__(self, params):
        self.params = params

    def encode(self):
        return "{0}?{1}".format(URL, urllib.urlencode(self.params))


def sign(host, secret_key, **kwargs):
    def _sign(**params):
        params.update(kwargs)
        sign_str = "GET{0}{1}?{2}".format(host, URL,
                                          "&".join("{0}={1}".format(encode(k), encode(params[k])) for k in
                                                   sorted(params.keys())))
        print(sign_str)
        hashed = hmac.new(secret_key, sign_str, sha1)
        sc = base64.encodestring(hashed.digest()).strip()
        params['Signature'] = sc
        return URLParer(params).encode()

    return _sign
