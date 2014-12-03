# -*- coding: utf-8 -*-
__author__ = 'wan'
import ConfigParser
import os


class ConfigUtil():
    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        path = os.path.join(os.getcwd(), "../conf/cloud.cfg")
        self.parser.read(path)

    def get_value(self, section, key):
        return self.parser.get(section, key)
