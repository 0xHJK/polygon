# -*- coding: utf-8 -*-

import sqlite3
from utils import TypeHelper, PolygonHelper
class IceDb():
    def __init__(self, **kwargs):
        #dbfile = kwargs.get('dbfile', 'ice.db')
        dbfile = kwargs.get('dbfile', '/lambda/app/ice.db')
        self.conn = sqlite3.connect(dbfile)

    def execute(self, sql):
        self.conn.execute(sql)
        self.conn.commit()

    def fetchall(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        self.conn.commit()
        return result

    def fetchone(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        self.conn.commit()
        return result

    def exit(self):
        self.conn.close()

class IceType():
    def __init__(self, **kwargs):
        self.tid = kwargs.get('tid', '00')
        self.tnote = kwargs.get('tnote', '所有类型')
    def get_tnote(self):
        idb = IceDb()
        sql = 'select tnote from ice_types where tid = "%s"' % self.tid
        self.tnote = idb.fetchone(sql)[0]
        idb.exit()
        return self.tnote

class IcePoi():
    def __init__(self, *args):
        self.pid = args[0]['id']
        self.name = args[0]['name']
        self.location = args[0]['location']
        self.adname = args[0]['adname']
        self.address = args[0]['address']
        self.poitype = args[0]['type']
        self.typecode = args[0]['typecode']
        self.rid = args[1]
    def save_to_db(self):
        sql = 'insert into ice_pois (pid, name, location, adname, address, poitype, typecode, rid) \
            values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
            (self.pid, self.name, self.location, self.adname, self.address, self.poitype, self.typecode, self.rid)
        idb = IceDb()
        idb.execute(sql)

class IceRecord():
    def __init__(self, **kwargs):
        self.rid = kwargs.get('rid', '')
        self.center = kwargs.get('center', '')
        self.polygon = kwargs.get('polygon', '')
        self.types = kwargs.get('types', '')
        self.tids = kwargs.get('tids', '')
        if self.polygon and self.types:
            self._set_record()

    def _fetchone(self, sql):
        idb = IceDb()
        result = idb.fetchone(sql)
        if not result:
            return None
        else:
            if isinstance(result, str):
                return result[0].split(',')
            return result[0]

    def _set_record(self):
        ph = PolygonHelper(self.polygon)
        self.polygon = ph.to_str()
        self.center = ph.get_center_str()
        th = TypeHelper(self.types)
        self.types = th.to_str()
        self.tids = th.get_tids_str()
        self.rid = ph.get_hash() + th.get_hash()

    def get_tids_by_rid(self, rid):
        sql = 'select tids from ice_records where rid = "%s"' % rid
        return self._fetchone(sql)

    def get_center_by_rid(self, rid):
        sql = 'select center from ice_records where rid = "%s"' % rid
        return self._fetchone(sql)

    def get_count(self):
        sql = 'select count(*) from ice_records'
        return self._fetchone(sql)

    def save_to_db(self):
        sql = 'insert into ice_records (rid, center, polygon, types, tids) \
            values ("%s", "%s", "%s", "%s", "%s")' % \
            (self.rid, self.center, self.polygon, self.types, self.tids)
        idb = IceDb()
        idb.execute(sql)

class IceDrumstick(object):
    def __init__(self, **kwargs):
        polygon = kwargs.get('polygon', '')
        types = kwargs.get('types', '')
        ph = PolygonHelper(polygon)
        th = TypeHelper(types)
        self.rid = ph.get_hash() + th.get_hash()
    def get_count(self):
        sql = 'select count(*) from ice_drumsticks'
        idb = IceDb()
        result = idb.fetchone(sql)
        return result[0]
    def save_to_db(self):
        sql = 'insert into ice_drumsticks (rid) values ("%s")' % (self.rid)
        idb = IceDb()
        idb.execute(sql)

        

if __name__ == '__main__':
    idb = IceDb()
    pt = IceType(tid = '05')
    print(pt.get_tnote())
    pi = IcePoi({
        "id":"B000A7BM4H","name":"肯德基(花家地店)","type":"餐饮服务;快餐厅;肯德基","typecode":"050301","address":"花家地小区1号商业楼","location":"116.469306,39.985589","pname":"北京市","cityname":"北京市","adname":"朝阳区"
    }, '23abc32f')
    pi.save_to_db()
    sql = 'select * from ice_pois'
    print(idb.fetchall(sql))

