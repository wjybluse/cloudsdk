# -*- coding: utf-8 -*-
__author__ = 'wan'
import logging
import os
import logging.handlers


class LogFactory():
    def __init__(self, cls):
        handler = logging.handlers.RotatingFileHandler(os.path.join(os.pardir, '../log/cloud.log'),
                                                       maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(pathname)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger(cls)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    @classmethod
    def logger(cls, name):
        """
        :rtype : LogFactory
        """
        return cls(name)

    def debug(self, *args):
        return self.logger.debug(" ".join([str(key) for key in args]))

    def info(self, *args):
        return self.logger.info(" ".join([str(key) for key in args]))

    def error(self, *args):
        return self.logger.exception(" ".join([str(key) for key in args]))

    def warn(self, *args):
        return self.logger.warning(" ".join([str(key) for key in args]))


def log(fn):
    def wrap(*args, **kwargs):
        logger = LogFactory.logger(__name__)
        # some args is not str
        tmp = [str(item) for item in args]
        logger.debug('Enter the method', '{0}({1})'.format(fn.__name__, ','.join(tmp) + "," + ','.join(
            (str(key) + '=' + str(val)) for key, val in kwargs.items())))
        return fn(*args, **kwargs)

    return wrap