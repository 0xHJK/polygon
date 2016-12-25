# -*- coding: utf-8 -*-

import os

from openpyxl import Workbook
from icemodel import IceDb, IceRecord
from utils import TypeHelper


class PoiCtrl():
    def __init__(self, **kwargs):
        self.tid = kwargs.get('tid', '01')
        self.rid = kwargs.get('rid', '')
    def get_location(self):
        idb = IceDb()
        if self.tid == '00':
            sql = 'select distinct location from ice_pois where rid = "' + self.rid + '"'
        else:
            sql = 'select distinct location from ice_pois where typecode like "' + self.tid + '%" and rid = "' + self.rid + '"'
        res = idb.fetchall(sql)
        result = [x[0].split(',') for x in res]
        return result

# 根据rid获得kvtypes和center
class RidCtrl():
    def __init__(self, rid):
        self.rid = rid

    def get_kvtypes(self):
        icr = IceRecord()
        tids = icr.get_tids_by_rid(self.rid).split(',')
        th = TypeHelper()
        return th.get_kvtypes(tids)

    def get_center(self):
        icr = IceRecord()
        center = icr.get_center_by_rid(self.rid)
        return center

class ExcelCtrl(object):
    def __init__(self, **kwargs):
        self.tid = kwargs.get('tid', '01')
        self.rid = kwargs.get('rid', '')
    def save_to_xlsx(self):
        idb = IceDb()
        os.chdir('/lambda/app/excel/')
        fname = self.rid + '_' + self.tid + '.xlsx'
        if self == '00':
            sql = 'select distinct * from ice_pois where rid = "' + self.rid + '"'
        else:
            sql = 'select distinct * from ice_pois where typecode like "' + self.tid + '%" and rid = "' + self.rid + '"'
        res = idb.fetchall(sql)
        wb = Workbook()
        ws = wb.active
        for row in res:
            ws.append(row)
        wb.save(filename = fname)
        return fname

        