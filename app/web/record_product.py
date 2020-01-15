#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/3 20:10.
"""
from operator import and_

from flask import request, jsonify
from sqlalchemy import func

from app.models.base import db
from app.models.product import Product
from app.models.record import Record
from app.models.record_product import RecordProduct
from app.utils.time_util import str2date
from app.web import web


@web.route ('/record_product/add', methods=['GET', 'POST'])
def record_product_add():
    record_product = RecordProduct ()
    record_product.set_attrs (request.args)
    db.session.add (record_product)
    db.session.commit ()
    print ('添加成功')
    return jsonify ({'code': 0})


@web.route ('/record_product/update', methods=['GET', 'POST'])
def record_product_update():
    id = request.args['id']
    record_product = RecordProduct.query.filter_by (id=id).first ()
    record_product.set_attrs (request.args)
    db.session.add (record_product)
    db.session.commit ()
    print ('更新成功')
    return jsonify ({'code': 0})


@web.route ('/record_product/delete', methods=['GET', 'POST'])
def record_product_delete():
    id = request.args['id']
    record_product = RecordProduct.query.filter_by (id=id).first ()
    db.session.delete (record_product)
    db.session.commit ()
    print ('删除成功')
    return jsonify ({'code': 0})


@web.route ('/record_product/get', methods=['GET', 'POST'])
def record_product_get_list():
    record_product_list = db.session.query (RecordProduct).filter ().all ()
    print (db.session.query (RecordProduct))
    record_product_json_list = RecordProduct.to_json_str (record_product_list)
    print (record_product_list)
    print (record_product_json_list)
    print ('列表返回成功')
    return jsonify (record_product_json_list)


#  SQL辅助函数
def to_get_record_product(filter_index, condition):
    p_s_list = db.session.query (Product.id.label ('pid'), Product.product_name.label ('pname'), func.sum (
        RecordProduct.change_amount).label ('amount1'),
                                 (func.sum (RecordProduct.price) * func.sum (
                                     RecordProduct.change_amount)).label ('price1')).join (Record,
                                                                                           Record.id == RecordProduct.record_id).join (
        Product, Product.id == RecordProduct.product_id).filter (condition, Record.operate_flag == 0).group_by (
        Product.id).subquery ()
    p_s_list2 = db.session.query (Product.id.label ('pid'), Product.image.label ('image'), func.sum (
        RecordProduct.change_amount).label ('amount2'),
                                  (func.sum (RecordProduct.price) * func.sum (RecordProduct.change_amount)).label (
                                      "price2")).join (Record,
                                                       Record.id == RecordProduct.record_id).join (
        Product, Product.id == RecordProduct.product_id).filter (condition, Record.operate_flag == 1).group_by (
        Product.id).subquery ()
    product_result_sql = db.session.query (p_s_list.c.pid, p_s_list.c.pname, p_s_list.c.amount1, p_s_list.c.price1,
                                           p_s_list2.c.amount2, p_s_list2.c.price2, p_s_list2.c.image).outerjoin (
        p_s_list2,
        p_s_list.c.pid == p_s_list2.c.pid)

    if filter_index == 0:
        return product_result_sql
    elif filter_index == 1:
        return product_result_sql.order_by ((p_s_list2.c.amount2 / p_s_list.c.amount1).desc ())
    elif filter_index == 2:
        return product_result_sql.order_by ((p_s_list2.c.amount2 / p_s_list.c.amount1).asc ())


# 返回数据封装辅助函数
def process_product_record(product_result):
    product_list_result = []
    detail_list_result = {}
    purchase_total_amount = 0
    purchase_total_price = 0.00
    sale_total_amount = 0
    sale_total_price = 0.00
    for product in product_result:
        product_desc = {}
        product_desc['id'] = product[0]
        product_desc['name'] = product[1]
        product_desc['pur_amount'] = int (product[2]) if product[2] is not None else 0
        product_desc['pur_price'] = product[3] if product[3] is not None else 0.00
        product_desc['sal_amount'] = int (product[4]) if product[4] is not None else 0
        product_desc['sal_price'] = product[5] if product[5] is not None else 0.00
        product_desc['image'] = product[6] if product[6] is not None else ''
        product_list_result.append (product_desc)

        purchase_total_amount += product_desc['pur_amount']  # 采购
        purchase_total_price += product_desc['pur_price']
        sale_total_amount += product_desc['sal_amount']  # 销售
        sale_total_price += product_desc['sal_price']
    detail_list_result['purchase_total_amount'] = purchase_total_amount
    detail_list_result['purchase_total_price'] = purchase_total_price
    detail_list_result['sale_total_amount'] = sale_total_amount
    detail_list_result['sale_total_price'] = sale_total_price
    result = {'product_list': product_list_result, 'detail_list': detail_list_result}
    return result


# 多条件联表查询
@web.route ('/record_product/search', methods=['GET', 'POST'])
def record_product_search():
    storage_id = request.args.get ("storage", type=int, default=None)  # 仓储编号 默认为第一个
    category_id = request.args.get ("category_id", type=int, default=None)  # 商品分类 默认为全部
    keywords = request.args.get ("keywords", type=str, default=None)  # 关键字搜索 默认为空
    filter_index = request.args.get ("filter_index", type=int, default=None)  # 筛选商品 默认为0

    start_date = str2date (request.args.get ("start_date", type=str, default=None))
    end_date = str2date (request.args.get ("end_date", type=str, default=None))
    print (type (storage_id), type (category_id), type (keywords), type (filter_index), type (start_date),
           type (end_date))
    print (storage_id, category_id, keywords, filter_index, start_date, end_date)
    condition = (Product.id > 0)
    if storage_id != 0 and storage_id is not None:
        condition = and_ (condition, Record.storage_id == storage_id)
    if category_id != 0 and category_id is not None:
        condition = and_ (condition, Product.category_id == category_id)
    if keywords != '' and keywords is not None:
        condition = and_ (condition, Product.product_name.like ("%" + keywords + "%"))
    if start_date is not None and end_date is not None:
        condition = and_ (condition, Record.operate_date.between (start_date, end_date))

    product_list = []
    detail_list = {}
    if filter_index == 0:
        print ('全部记录')
        product_result_sql = to_get_record_product (filter_index, condition)
        print ('product_result_sql: ' + str (product_result_sql))
        product_result = product_result_sql.all ()
        print ('product_result: ' + str (product_result))
        product_list = process_product_record (product_result)['product_list']
        detail_list = process_product_record (product_result)['detail_list']

    elif filter_index == 1:
        print ('畅销榜')
        product_result = to_get_record_product (filter_index, condition)
        print ('product_result_sql: ' + str (product_result))
        product_result = product_result.all ()
        print ('product_result: ' + str (product_result))
        product_list = process_product_record (product_result)['product_list']
        detail_list = process_product_record (product_result)['detail_list']

    elif filter_index == 2:
        print ('滞销榜')
        product_result = to_get_record_product (filter_index, condition)
        print ('product_result_sql: ' + str (product_result))
        product_result = product_result.all ()
        print ('product_result: ' + str (product_result))
        product_list = process_product_record (product_result)['product_list']
        detail_list = process_product_record (product_result)['detail_list']

    return jsonify ({'code': 0, 'result': product_list, 'sts_result': detail_list})
