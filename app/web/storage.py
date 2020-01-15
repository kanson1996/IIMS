#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/8 21:51.
"""

from flask import request, jsonify

from app.models.base import db
from app.models.product import Product
from app.models.storage import Storage
from app.web import web


@web.route ('/storage/add', methods=['GET', 'POST'])
def storage_add():
    storage = Storage ()
    storage.storage_priority = request.args['priority'] if request.args['priority'] is not None else ''
    storage.storage_name = request.args['name']
    db.session.add (storage)
    db.session.commit ()
    print ('添加成功')
    return jsonify ({'code': 0})


@web.route ('/storage/update', methods=['GET', 'POST'])
def storage_update():
    id = request.args['id']
    storage_name = request.args['name']
    storage_priority = request.args['priority']
    print (id)
    print (storage_name)
    print (storage_priority)
    storage = Storage.query.filter_by (id=id).first ()
    storage.storage_name = storage_name
    storage.storage_priority = storage_priority
    db.session.add (storage)
    db.session.commit ()
    print ('更新成功')
    return jsonify ({'code': 0})


@web.route ('/storage/delete', methods=['GET', 'POST'])
def storage_delete():
    id = request.args['id']
    storage = Storage.query.filter_by (id=id).first ()
    db.session.delete (storage)
    db.session.commit ()
    print ('删除成功')
    return jsonify ({'code': 0})


@web.route ('/storage/get', methods=['GET', 'POST'])
def storage_get_list():
    storage_list = db.session.query (Storage).filter ().all ()
    print (db.session.query (Storage))
    storage_json_list = Storage.to_json_str (storage_list)
    print (storage_list)
    print (storage_json_list)
    print ('列表返回成功')
    return jsonify ({'result': storage_json_list})


@web.route ('/storage/search', methods=['GET', 'POST'])
def storage_search():
    id = request.args['id']
    print ("id:" + id)
    storage = Storage.query.filter_by (id=id).first ()
    return jsonify ({'result': {'id': id, 'name': storage.storage_name, 'priority': storage.storage_priority}})


# 模糊搜索
@web.route ('/storage/searchByKey', methods=['GET', 'POST'])
def storage_search_by_key():
    keywords = request.args['keywords']
    print ("keywords:" + keywords)
    storage_list = Storage.query.filter (
        Storage.storage_name.like ("%" + keywords + "%") if keywords is not None else "").all ()
    storage_json_list = Storage.to_json_str (storage_list)
    return jsonify ({'result': storage_json_list})


# 按仓储查询包含的商品
@web.route ('/product/searchByStorage', methods=['GET', 'POST'])
def product_search_by_storage():
    # 查询指定的仓储有几个商品
    storage_id = request.args['storage']
    storage = Storage.query.filter_by (id=storage_id).first ()
    product_list = storage.products
    for product in product_list:
        print (product.product_name)
    product_json_list = Product.to_json_str (product_list)
    return jsonify ({'result': product_json_list})
