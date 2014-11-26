# -*- coding: utf-8 -*-
# AWSContext provider context for aws auth
# current support all AWS signature method
#Notice:don't change the signature method
#
__author__ = 'wan'
import datetime
import hashlib
import hmac
import urllib
import base64
from cloudsdk.api.context import AuthContext


METHOD = 'GET'
ENCODING = 'utf-8'
ALGORITHM = 'AWS4-HMAC-SHA256'
SIGNED_HEADERS = 'host;x-amz-date'
t = datetime.datetime.utcnow()
date_stamp = t.strftime('%Y%m%d')


class AWSContext(AuthContext):
    def __init__(self, access_key, secret_key, host='localhost', port=80, region=None, **kwargs):
        AuthContext.__init__(self, access_key, secret_key, host=host, port=port, region=region, **kwargs)
        self.service_name = None
        self.headers = {}

    def get_context(self):
        params = dict(Version='2013-10-15')

        # support v4 sign method,the current signature is add header for request
        def _sign_v4(**kwargs):
            """
            sign method is complex,if you want to known more,please visit
            http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
            :param kwargs: the request params
            :return:the request string and the headers
            """
            kwargs.update(params)
            aws_data = t.strftime('%Y%m%dT%H%M%SZ')
            q_str = '&'.join('{0}={1}'.format(k, kwargs[k]) for k in sorted(kwargs.keys()))
            canonical_headers = 'host:{0}\nx-amz-date:{1}\n'.format(self.host, aws_data)
            payload_hash = hashlib.sha256('').hexdigest()
            sign_request = 'GET\n/\n{0}\n{1}\n{2}\n{3}'.format(q_str, canonical_headers, SIGNED_HEADERS, payload_hash)
            credential_scope = '{0}/{1}/{2}/aws4_request'.format(date_stamp, self.region, self.service_name)
            sign_str = '{0}\n{1}\n{2}\n{3}'.format(ALGORITHM, aws_data, credential_scope,
                                                   hashlib.sha256(sign_request).hexdigest())
            signing_key = _create_key(self.secret_key, self.region, self.service_name)
            signature = hmac.new(signing_key, sign_str.encode(ENCODING), hashlib.sha256).hexdigest()
            headers_str = '{0} Credential={1}/{2},SignedHeaders={3},Signature={4}'.format(ALGORITHM, self.access_key,
                                                                                          credential_scope,
                                                                                          SIGNED_HEADERS, signature)
            self.headers = {'x-amz-date': aws_data, 'Authorization': headers_str}
            return '?{0}'.format(q_str)

        #return _sign_v2(self.secret_key, self.host, self.access_key)
        return _sign_v4

    def get_headers(self):
        return self.headers

    def set_service(self, service):
        self.service_name = service


def _create_key(secret_key, region, service_name):
    k_data = hashed(('AWS4' + secret_key).encode(ENCODING), date_stamp)
    k_region = hashed(k_data, region)
    k_service = hashed(k_region, service_name)
    k_sign = hashed(k_service, 'aws4_request')
    return k_sign


def hashed(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


class URLParser():
    def __init__(self, params):
        self.params = params

    def encode(self):
        return urllib.urlencode(self.params)


# support v2 sign method
# the signature add to url
def _sign_v2(secret_key, host, access_key):
    params = dict(SignatureVersion=2, SignatureMethod='HmacSHA256', Timestamp=datetime.datetime.utcnow().isoformat(),
                  Version='2013-10-15', AWSAccessKeyId=access_key)

    def _sign(**kwargs):
        params.update(kwargs)
        data = []
        for key, val in params.items():
            data.append((key, val))
        sorted_query = sorted(data)
        url = urllib.urlencode(sorted_query).replace('+', '%20')
        sign_to_str = 'GET\n{0}\n/\n{1}'.format(host, url)
        signature = hmac.new(key=secret_key, msg=sign_to_str, digestmod=hashlib.sha256).digest()
        signature = base64.encodestring(signature).strip()
        urlencoded_signature = urllib.quote_plus(signature)
        return '?{0}&Signature={1}'.format(url, urlencoded_signature)

    return _sign
