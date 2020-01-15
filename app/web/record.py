#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/3 20:10.
"""
import json

from flask import request, jsonify

from app.models.base import db
from app.models.record import Record
from app.models.record_product import RecordProduct
from app.models.storage_product import StorageProduct
from app.web import web
from test.uuid import tid_maker


@web.route ('/record/add', methods=['GET', 'POST'])
def record_add():
    record_id = tid_maker ()
    purchase_data = json.loads (request.get_data ())  # request.args['products'] #str # dict
    record = Record ()
    record_list = purchase_data['records']
    record_list = record_list[0]  # 传回的record信息
    record.set_attrs (record_list)
    record.id = record_id  # 添加自定义的id
    product_list = purchase_data['products']
    flag = record_list['operate_flag']
    for product in product_list:
        record_product = RecordProduct ()
        record_product.record_id = record_id
        record_product.product_id = product['id']
        if flag != 2:
            record_product.change_amount = product['number']
        else:
            record_product.change_amount = product['check_counts']

        new_storage_id = None
        if flag == 0:
            record_product.price = product['purchase_price']
            new_storage_id = record_list['storage_id']
        elif flag == 1:
            record_product.price = product['retail_price']
            new_storage_id = product['storage_id']
        elif flag == 2:
            record_product.price = product['purchase_price']
            new_storage_id = record_list['storage_id']
        product_storage_info = StorageProduct.query.filter_by (storage_id=new_storage_id,
                                                               product_id=product['id']).first ()
        if product_storage_info:
            if flag == 0:
                product_storage_info.product_amount += product['number']
            elif flag == 1:
                product_storage_info.product_amount -= product['number']
            elif flag == 2:
                product_storage_info.product_amount += product['check_counts']
            db.session.commit ()
        else:
            storage_product = StorageProduct ()  # 这个变更记录的商品id是从1对1 的record_product中拿到的，仓储id是从record中取得的
            storage_product.product_id = product['id']
            storage_product.storage_id = new_storage_id
            storage_product.product_amount = product['number']
            db.session.add (storage_product)

        record.records.append (record_product)  # 循环尾部添加record_product
    db.session.add (record)
    db.session.commit ()
    print ('添加成功')
    return jsonify ({'code': 0})


@web.route ('/record/update', methods=['GET', 'POST'])
def record_update():
    id = request.args['id']
    record = Record.query.filter_by (id=id).first ()
    record.set_attrs (request.args)
    db.session.add (record)
    db.session.commit ()
    print ('更新成功')
    return jsonify ({'code': 0})


@web.route ('/record/delete', methods=['GET', 'POST'])
def record_delete():
    id = request.args['id']
    record = Record.query.filter_by (id=id).first ()
    db.session.delete (record)
    db.session.commit ()
    print ('删除成功')
    return jsonify ({'code': 0})


@web.route ('/record/get', methods=['GET', 'POST'])
def record_get_list():
    record_list = db.session.query (Record).filter ().all ()
    print (db.session.query (Record))
    record_json_list = Record.to_json_str (record_list)
    print (record_list)
    print (record_json_list)
    print ('列表返回成功')
    return jsonify (record_json_list)
