# -*- coding: utf-8 -*-

import re
import hashlib

# from icemodel import IceType

def md5gen(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()[:6]

class PolygonHelper():
    def __init__(self, *args):
        if args:
            self.s = args[0]

    def to_list(self):
        # 将中文逗号转换成英文逗号，清除空格
        s = self.s.replace('，', ',').replace(' ', '')
        return re.findall('\d+\.\d{3,6}\,\d+\.\d{3,6}', s)

    def to_str(self):
        return ';'.join(self.to_list())

    def get_center_list(self):
        lngs, lats = [], []
        for si in self.to_list():
            lngs.append(float(si.split(',')[0]))
            lats.append(float(si.split(',')[1]))
        lng_ave = round((max(lngs) + min(lngs)) / 2, 6)
        lat_ave = round((max(lats) + min(lats)) / 2, 6)
        return [lng_ave, lat_ave]

    def get_center_str(self):
        center = [str(x) for x in self.get_center_list()]
        return ','.join(center)

    def get_hash(self):
        return md5gen(self.to_str())


class TypeHelper():
    def __init__(self, *args):
        if args:
            self.s = args[0]

    def to_list(self):
        # 匹配六个数字
        return re.findall('\d{6}', self.s)

    def to_str(self):
        return '|'.join(self.to_list())

    def get_tids(self):
        tids_list = [x[:2] for x in self.to_list()]
        return sorted(list(set(tids_list)))

    def get_tids_str(self):
        return ','.join(self.get_tids())

    def get_kvtypes(self, *args):
        if not args:
            tids = self.get_tids()
        else:
            tids = args[0]
        from icemodel import IceType
        # if isinstance(tids, str):
        #     ict = IceType(tid = tids)
        #     return(tids, ict.get_tnote())
        # elif isinstance(tids, list):
        for tid in tids:
            ict = IceType(tid = tid)
            yield (tid, ict.get_tnote())

    def get_hash(self):
        return md5gen(self.to_str())
