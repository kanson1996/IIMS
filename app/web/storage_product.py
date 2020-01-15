#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/3 20:10.
"""
from flask import request, jsonify

from app.models.base import db
from app.models.storage_product import StorageProduct
from app.web import web


@web.route ('/storage_product/add', methods=['GET', 'POST'])
def storage_product_add():
    storage_product = StorageProduct ()
    storage_product.set_attrs (request.args)
    db.session.add (storage_product)
    db.session.commit ()
    print ('添加成功')
    return jsonify ({'code': 0})


@web.route ('/storage_product/update', methods=['GET', 'POST'])
def storage_product_update():
    id = request.args['id']
    storage_product = StorageProduct.query.filter_by (id=id).first ()
    storage_product.set_attrs (request.args)
    db.session.add (storage_product)
    db.session.commit ()
    print ('更新成功')
    return jsonify ({'code': 0})


@web.route ('/storage_product/delete', methods=['GET', 'POST'])
def storage_product_delete():
    id = request.args['id']
    storage_product = StorageProduct.query.filter_by (id=id).first ()
    db.session.delete (storage_product)
    db.session.commit ()
    print ('删除成功')
    return jsonify ({'code': 0})


@web.route ('/storage_product/get', methods=['GET', 'POST'])
def storage_product_get_list():
    storage_product_list = db.session.query (StorageProduct).filter ().all ()
    print (db.session.query (StorageProduct))
    storage_product_json_list = StorageProduct.to_json_str (storage_product_list)
    print (storage_product_list)
    print (storage_product_json_list)
    print ('列表返回成功')
    return jsonify (storage_product_json_list)


@web.route ('/storage_product/search', methods=['GET', 'POST'])
def storage_product_search():
    pass
