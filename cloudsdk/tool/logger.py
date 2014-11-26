# -*- coding: utf-8 -*-
__author__ = 'wan'
import logging
import logging.handlers


class LogFactory():
    def __init__(self, cls):
        handler = logging.handlers.RotatingFileHandler('cloud.log', maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(pathname)s:%(thread)d - %(name)s - %(message)s'
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
        return self.logger.error(" ".join([str(key) for key in args]))

    def warn(self, *args):
        return self.logger.warning(" ".join([str(key) for key in args]))