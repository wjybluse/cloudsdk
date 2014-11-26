# -*- coding: utf-8 -*-
__author__ = 'wan'
import uuid
import hmac
import base64
import urllib
import time
from hashlib import sha1
from cloudsdk.tool.util import encode
from cloudsdk.api.context import AuthContext
from cloudsdk.tool.logger import LogFactory

logger = LogFactory.logger(__name__)
timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
API_VERSION = '2013-01-10'
ENCODING = 'UTF-8'
RSP_FORMAT = 'JSON'
SING_VERSION = '1.0'
SIGN_METHOD = 'HMAC-SHA1'


class AliContext(AuthContext):
    def get_context(self):
        params = dict(Version=API_VERSION, AccessKeyId=self.access_key, TimeStamp=timestamp, Format=RSP_FORMAT,
                      SignatureVersion=SING_VERSION, SignatureNonce=str(uuid.uuid1()), SignatureMethod=SIGN_METHOD)
        if self.region is not None:
            params['RegionId'] = self.region

        def sign(**kwargs):
            for key, val in kwargs.items():
                params[key] = val
            signature = _signature(self.secret_key, **params)
            params['Signature'] = signature
            return URLParser(params).encode()

        return sign

    def get_headers(self):
        return {}


class URLParser():
    def __init__(self, params):
        self.params = params

    def encode(self):
        url = '/?' + urllib.urlencode(self.params)
        logger.info("current url", url)
        return url


def _signature(secret, **params):
    sign = 'GET&%2F&{0}'.format(
        encode("&".join("{0}={1}".format(encode(key), encode(params[key])) for key in sorted(params.keys()))))
    h = hmac.new("{0}&".format(secret), sign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature
