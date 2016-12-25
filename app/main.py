#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, Response, render_template, request, send_from_directory, abort

from icemap import IceMap
from icectrl import PoiCtrl, RidCtrl, ExcelCtrl
from icemodel import IceRecord, IceDrumstick
from utils import PolygonHelper, TypeHelper

app = Flask(__name__)

@app.route('/excel/<filename>')
def download(filename):
    if request.method == 'GET':
        return send_from_directory('excel', filename, as_attachment = True)
        abort(404)

@app.route('/', methods = ['GET', 'POST'])
def index():
    icd = IceDrumstick()
    count = int(icd.get_count()) + 5
    return render_template('index.html', count = count)

@app.route('/view/<rid>', methods = ['GET'])
def view(rid):
    # 根据rid从ice_records表中获得tids
    rc = RidCtrl(rid)
    kvtypes = rc.get_kvtypes()
    center = rc.get_center()
    if kvtypes and center:
        return render_template('view.html',
            kvtypes = kvtypes,
            center = center,
            rid = rid)
    else:
        abort(404)
    # 根据rid从ice_pois表中获得pois

@app.route('/api', methods = ['GET', 'POST'])
def api():
    # POST请求：传递types和polygon给后端处理
    if request.method == 'POST':
        types = request.form['types']
        polygon = request.form['polygon']
        if request.form['do'] == 'lbs':
            icd = IceDrumstick(types = types, polygon = polygon)
            icd.save_to_db()
            im = IceMap(types = types, polygon = polygon)
            im.save_data()
            icr = IceRecord(types = types, polygon = polygon)
            icr.save_to_db()
            return icr.rid
        else:
            ph = PolygonHelper(polygon)
            th = TypeHelper(types)
            return ph.get_hash() + th.get_hash()
    # GET请求
    # do=view: 返回数据给前端展示
    if request.method == 'GET':
        tid = request.args.get('tid')
        rid = request.args.get('rid')
        if request.args.get('do') == 'view':
            pc = PoiCtrl(tid = tid, rid = rid)
            return Response(json.dumps(pc.get_location()), mimetype='application/json')

    # do=excel: 生成excel表
        elif request.args.get('do') == 'excel':
            ec = ExcelCtrl(tid = tid, rid = rid)
            return ec.save_to_xlsx()



if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')

