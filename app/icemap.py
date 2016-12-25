# -*- coding:utf-8 -*-

import threading
import requests
from icemodel import IcePoi
from utils import PolygonHelper, TypeHelper

class IceMap():
    def __init__(self, **kwargs):
        types = kwargs.get('types', '050000')
        polygon = kwargs.get('polygon', '120.107076,30.326175;120.085948,30.316822;')
        th = TypeHelper(types)
        ph = PolygonHelper(polygon)
        self.types_list = th.to_list()
        self.polygon = ph.to_str()
        self.rid = ph.get_hash() + th.get_hash()
        self.key = 'e444f2d824f09ff1708854c1e66d0e19'
        self.offset = 20
        self.url = 'http://restapi.amap.com/v3/place/polygon'
        self.lock = threading.Lock()

    def reqs(self, *args):
        data = dict(
            key = self.key,
            polygon = self.polygon,
            offset = self.offset,
            types = args[0],
            page = args[1]
        )
        r = requests.get(self.url, data)
        return r.json()

    def save_to_db(self, pois):
        for poi in pois:
            pi = IcePoi(poi, self.rid)
            self.lock.acquire()
            pi.save_to_db()
            self.lock.release()

    def lbs_handler(self, types):
        for t in types:
            page = 1
            while True:
                res = self.reqs(t, page)
                count = int(res['count'])
                print(t, page, count)
                self.save_to_db(res['pois'])
                if page * self.offset >= count:
                    break
                page += 1

    def save_data(self):
        all_threads = []
        for i in range(0, len(self.types_list), 20):
            t = threading.Thread(target = self.lbs_handler, args = (self.types_list[i: i+20],))
            all_threads.append(t)
            t.start()
        for t in all_threads:
            t.join()



if __name__ == '__main__':
    im = IceMap()
    im.save_data()

