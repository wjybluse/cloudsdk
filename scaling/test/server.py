# -*- coding: utf-8 -*-
__author__ = 'wan'
from scaling.rest.rest import RestServer

if __name__ == '__main__':
    server = RestServer(port=30000)
    server.start()