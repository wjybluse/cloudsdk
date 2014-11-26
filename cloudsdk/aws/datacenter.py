# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.datacenter import DCSupport
from cloudsdk.rest.request import Request
from _xml import XmlParser
from _xml import validate_rsp
from _xml import find_all


class AWSDCSupport(DCSupport):
    def __init__(self, ctx):
        DCSupport.__init__(self, ctx)
        ctx.service_name = 'ec2'
        self.request = Request(ctx)

    def list_regions(self):
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='DescribeRegions')
        validate_rsp(rsp, 'DescribeRegions')
        return find_all(rsp, 'regionName')

    def list_zones(self):
        rsp = self.request.invoke(scheme='https', callback=XmlParser.parser, Action='DescribeAvailabilityZones')
        validate_rsp(rsp, 'DescribeAvailabilityZones')
        return find_all(rsp, 'zoneName')
