# -*- coding: utf-8 -*-
__author__ = 'wan'
from setuptools import setup

setup(name='cloudsdk',
      version='1.0',
      description='cloud sdk provider simple interface for different cloud,like AWS,ALI,QCLOUD',
      author='Elians Wan',
      author_email='wantingyi@sina.com',
      license='MIT',
      packages=['cloudsdk', '_scaling'],
      install_requires=[
          'PyMongo',
          'azure'
      ],
      zip_safe=False)
