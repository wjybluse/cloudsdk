# -*- coding: utf-8 -*-
__author__ = 'wan'
from cloudsdk.api.datacenter import DCSupport
from _base import validate_rsp


class AliDCSupport(DCSupport):
    def list_regions(self):
        rsp = self.request.invoke(Action='DescribeRegions')
        validate_rsp(rsp, 'DescribeRegions')
        rsp = eval(rsp)
        region = eval(rsp)['Regions']
        if region is None or len(region) <= 0:
            return None
        region_ids = []
        for r in region['Region']:
            region_ids.append(r['RegionId'])
        return region_ids


    def list_zones(self):
        rsp = self.request.invoke(Action='DescribeZones')
        validate_rsp(rsp, 'DescribeZones')
        rsp = eval(rsp)
        zone = eval(rsp)['Zones']
        if zone is None or len(zone) <= 0:
            return None
        zones = []
        for z in zone['Zone']:
            zones.append(z['ZoneId'])
        return zones
