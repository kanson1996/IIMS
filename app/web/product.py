#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/2 17:32.
"""

import os

from flask import jsonify, request, render_template, flash
from sqlalchemy import and_, func

from app.models.base import db
from app.models.category import Category
from app.models.product import Product
from app.models.storage_product import StorageProduct
from app.utils.uuid import tid_maker
from . import web


@web.route ('/product/add', methods=['GET', 'POST'])
def product_add():
    product = Product ()
    product.id = request.args['id']
    product.product_name = request.args['product_name']
    product.image = request.args['image']
    product.serial_code = request.args['serial_code']
    product.specification = request.args['specification'] if request.args['specification'] != '' else 0
    product.factory_price = request.args['factory_price'] if request.args['factory_price'] != '' else 0.00
    product.sale_price = request.args['sale_price'] if request.args['sale_price'] != '' else 0.00
    product.sequence = request.args['sequence'] if request.args['sequence'] != '' else 0
    product.pre_warning_value = request.args['pre_warning_value'] if request.args['pre_warning_value'] != '' else 0
    product.note = request.args['note'] if request.args['note'] != '' else ''
    product.category_id = (None if request.args['category_id'] == '' else request.args['category_id'])
    db.session.add (product)
    db.session.commit ()
    print ('添加成功')
    return jsonify ({'code': 0})


@web.route ('/product/update', methods=['GET', 'POST'])
def product_update():
    id = request.args['id']
    product = Product.query.filter_by (id=id).first ()  # 根据id查询到原商品信息
    product.product_name = request.args['product_name']
    product.image = request.args['image']
    product.serial_code = request.args['serial_code']
    product.specification = request.args['specification']
    product.factory_price = request.args['factory_price']
    product.sale_price = request.args['sale_price']
    product.sequence = request.args['sequence']
    product.pre_warning_value = request.args['pre_warning_value']
    product.note = request.args['note']
    product.category_id = request.args['category_id'] if request.args['category_id'] != '' else 0
    db.session.add (product)
    db.session.commit ()
    print ('更新成功')
    return jsonify ({'code': 0})


@web.route ('/product/delete', methods=['GET', 'POST'])
def product_delete():
    id = request.args['id']
    product = Product.query.filter_by (id=id).first ()
    db.session.delete (product)
    db.session.commit ()
    print ('删除成功')
    return jsonify ({'code': 0})


@web.route ('/product/get', methods=['GET', 'POST'])
def product_get_list():
    storage_id = request.args.get ("storage", type=int, default=None)  # 仓储编号 默认为第一个
    category_id = request.args.get ("category_id", type=int, default=None)  # 商品分类 默认为全部
    keywords = request.args.get ("keywords", type=str, default=None)  # 关键字搜索 默认为空
    filter_index = request.args.get ("filter_index", type=int, default=None)  # 筛选商品 默认为0
    start_date = request.args.get ("start_date", type=str, default=None)
    end_date = request.args.get ("end_date", type=str, default=None)
    
    result_list = list ()  # []

    condition = (1 == 1)
    if category_id != 0 and category_id is not None:
        condition = and_ (condition, Product.category_id == category_id)
    if keywords != '' and keywords is not None:
        condition = and_ (condition, Product.product_name.like ("%" + keywords + "%"))
    if filter_index == 0:
        print ('全部商品')
    elif filter_index == 2:
        print ('只看有库存商品')
        condition = and_ (condition, StorageProduct.product_amount > 0)
    elif filter_index == 3:
        print ('只看预警商品')
        condition = and_ (condition, StorageProduct.product_amount < Product.pre_warning_value)
    elif filter_index == 1:
        print ('根据商品名排序')
    my_list = []
    if storage_id == 0:
        print (0)
        query_sql = db.session.query (Product.id.label ('id'), Product.image.label ('image'),
                                      Product.category_id.label ('category_id'),
                                      Product.factory_price.label ('factory_price'),
                                      Product.sale_price.label ('sale_price'),
                                      Product.product_name.label ('product_name'),
                                      StorageProduct.product_amount.label ('product_amount'),
                                      Product.pre_warning_value.label ('pre_warning_value')).outerjoin (StorageProduct,
                                                                                                        Product.id == StorageProduct.product_id).filter (
            condition).subquery ()
        query_all = db.session.query (query_sql.c.id, query_sql.c.image, query_sql.c.category_id,
                                      query_sql.c.factory_price,
                                      query_sql.c.sale_price, query_sql.c.product_name,
                                      func.sum (query_sql.c.product_amount).label ('product_amount'),
                                      query_sql.c.pre_warning_value).group_by (
            query_sql.c.id)
        print ('==========sql==========')
        print (query_all)
        if filter_index == 1:
            result_list = query_all.order_by (query_sql.c.product_name.asc ()).all ()
        else:
            result_list = query_all.all ()
        print (result_list)
        for result in result_list:
            item = {}
            item['id'] = result.id
            item['image'] = result.image if result.image is not None else ''
            item['category_id'] = result.category_id
            item['factory_price'] = result.factory_price if result.factory_price is not None else 0.00
            item['sale_price'] = result.sale_price if result.sale_price is not None else 0.00
            item['product_name'] = result.product_name
            item['product_amount'] = int (result.product_amount) if result.product_amount is not None else 0
            item['pre_warning_value'] = int (result.pre_warning_value) if result.pre_warning_value is not None else 0
            my_list.append (item)

    else:
        if storage_id != 0 and storage_id is not None:
            condition = and_ (condition, StorageProduct.storage_id == storage_id)
        query = db.session.query (Product, StorageProduct).outerjoin (StorageProduct,
                                                                      Product.id == StorageProduct.product_id).filter (
            condition)
        print (query)
        if filter_index == 1:
            result_list = query.order_by (Product.product_name.asc ()).all ()
        else:
            result_list = query.all ()
        print (result_list)
        for result in result_list:
            product = result[0]
            storageproduct = result[1]
            item = {}
            item['id'] = product.id
            item['image'] = product.image
            item['category_id'] = product.category_id
            item['storage_id'] = storageproduct.storage_id if storageproduct is not None else 0
            item['factory_price'] = product.factory_price
            item['sale_price'] = product.sale_price
            item['product_name'] = product.product_name
            item['product_amount'] = storageproduct.product_amount if storageproduct is not None else 0
            item['pre_warning_value'] = int (product.pre_warning_value) if product.pre_warning_value is not None else 0
            my_list.append (item)

    return jsonify ({'code': 0, 'result': my_list})


@web.route ('/product/search', methods=['GET', 'POST'])
def product_search():
    id = request.args['id']
    print ("id:" + id)
    product = Product.query.filter_by (id=id).first ()  # 查询指定的商品
    category_id = product.category_id
    product = product.dobule_to_dict ()
    if category_id is not None:
        category = Category.query.filter_by (id=category_id).first ()
        print (category.category_name)
        product['category_name'] = category.category_name
    return jsonify ({'result': product})


# 模糊搜索
@web.route ('/product/searchByKey', methods=['GET', 'POST'])
def product_search_by_key():
    keywords = request.args['keywords']
    print ("keywords:" + keywords)
    product_list = Product.query.filter (
        Product.product_name.like ("%" + keywords + "%") if keywords is not None else "").all ()
    product_json_list = Product.to_json_str (product_list)
    return jsonify ({'result': product_json_list})


# 按类别查询
@web.route ('/product/searchByCategory', methods=['GET', 'POST'])
def product_search_by_category():
    category_id = request.args['category_id']
    print ("category_id:" + category_id)
    product_list = Product.query.filter_by (category_id=category_id).all ()
    product_json_list = Product.to_json_str (product_list)
    return jsonify ({'result': product_json_list})


@web.route ('/product/upload', methods=['GET', 'POST'])
def product_upload():
    filePath = request.args['filePath']
    name = request.args['name']
    return jsonify ({'code': 0})


# 多条件联表查询
@web.route ('/product/multiple_tags', methods=['GET', 'POST'])
def product_multiple_tags():
    storage_id = request.args.get ("storage", type=int, default=None)  # 仓储编号 默认为第一个
    category_id = request.args.get ("category_id", type=int, default=None)  # 商品分类 默认为全部
    keywords = request.args.get ("keywords", type=str, default=None)  # 关键字搜索 默认为空
    filter_index = request.args.get ("filter_index", type=int, default=None)  # 筛选商品 默认为0
    start_date = request.args.get ("start_date", type=str, default=None)
    end_date = request.args.get ("end_date", type=str, default=None)
    
    result_list = list ()  # []

    condition = (1 == 1)
    if storage_id != 0 and storage_id is not None:
        condition = and_ (condition, StorageProduct.storage_id == storage_id)
    if category_id != 0 and category_id is not None:
        condition = and_ (condition, Product.category_id == category_id)
    if keywords != '' and keywords is not None:
        condition = and_ (condition, Product.product_name.like ("%" + keywords + "%"))

    if filter_index == 0:
        print ('全部商品')
    elif filter_index == 2:
        print ('只看有库存商品')
        condition = and_ (condition, StorageProduct.product_amount > 0)
    elif filter_index == 3:
        print ('只看预警商品')
        condition = and_ (condition, StorageProduct.product_amount < Product.pre_warning_value)
    elif filter_index == 1:
        print ('根据商品名排序')

    query = db.session.query (Product, StorageProduct).outerjoin (StorageProduct,
                                                                  Product.id == StorageProduct.product_id).filter (
        condition)
    print (query)
    if filter_index == 1:
        result_list = query.order_by (Product.product_name.asc ()).all ()
    else:
        result_list = query.all ()

    my_list = []
    for result in result_list:
        product = result[0]
        storageproduct = result[1]
        item = {}
        item['id'] = product.id
        item['image'] = product.image
        item['category_id'] = product.category_id
        item['storage_id'] = storageproduct.storage_id if storageproduct is not None else 0
        item['factory_price'] = product.factory_price
        item['sale_price'] = product.sale_price
        item['product_name'] = product.product_name
        item['product_amount'] = storageproduct.product_amount if storageproduct is not None else 0
        my_list.append (item)
    return jsonify ({'code': 0, 'result': my_list})


# 多条件联表查询
@web.route ('/product/purchase', methods=['GET', 'POST'])
def product_purchase():
    category_id = request.args.get ("category_id", type=int, default=None)  # 商品分类 默认为全部
    keywords = request.args.get ("keywords", type=str, default=None)  # 关键字搜索 默认为空
    filter_index = request.args.get ("filter_index", type=int, default=None)  # 筛选商品 默认为0
    start_date = request.args.get ("start_date", type=str, default=None)
    end_date = request.args.get ("end_date", type=str, default=None)
    
    result_list = list ()  # []

    condition = (1 == 1)
    if category_id != 0 and category_id is not None:
        condition = and_ (condition, Product.category_id == category_id)
    if keywords != '' and keywords is not None:
        condition = and_ (condition, Product.product_name.like ("%" + keywords + "%"))

    if filter_index == 0:
        print ('全部商品')
    elif filter_index == 2:
        print ('只看有库存商品')
        condition = and_ (condition, StorageProduct.product_amount > 0)
    elif filter_index == 3:
        print ('只看预警商品')
        condition = and_ (condition, StorageProduct.product_amount < Product.pre_warning_value)
    elif filter_index == 1:
        print ('根据商品名排序')

    query_sql = db.session.query (Product.id.label ('id'), Product.image.label ('image'),
                                  Product.category_id.label ('category_id'),
                                  Product.factory_price.label ('factory_price'),
                                  Product.sale_price.label ('sale_price'),
                                  Product.product_name.label ('product_name'),
                                  StorageProduct.product_amount.label ('product_amount')).outerjoin (StorageProduct,
                                                                                                     Product.id == StorageProduct.product_id).filter (
        condition).subquery ()
    query_all = db.session.query (query_sql.c.id, query_sql.c.image, query_sql.c.category_id, query_sql.c.factory_price,
                                  query_sql.c.sale_price, query_sql.c.product_name,
                                  func.sum (query_sql.c.product_amount).label ('product_amount')).group_by (
        query_sql.c.id)
    print (query_all)
    if filter_index == 1:
        result_list = query_all.order_by (Product.product_name.asc ()).all ()
    else:
        result_list = query_all.all ()

    my_list = []
    for result in result_list:
        item = {}
        item['id'] = result.id
        item['image'] = result.image if result.image is not None else ''
        item['category_id'] = result.category_id
        item['factory_price'] = result.factory_price if result.factory_price is not None else 0.00
        item['sale_price'] = result.sale_price if result.sale_price is not None else 0.00
        item['product_name'] = result.product_name
        item['product_amount'] = int (result.product_amount) if result.product_amount is not None else 0
        my_list.append (item)
    return jsonify ({'code': 0, 'result': my_list})


@web.route ('/api/v1/product/upload', methods=['GET', 'POST'])
def editorData():
    # 获取图片文件 name = file
    upload_file = request.files['file']
    # 获取图片名
    file_name = upload_file.filename
    # 生成随机字符串，防止图片名字重复
    ran_str = tid_maker ()
    # 图片名称 给图片重命名 为了图片名称的唯一性
    file_name = ran_str + '.' + file_name.split ('.')[-1]
    # 文件保存目录（定义一个根目录 用于保存图片用）
    file_path = r'E:/images'
    if upload_file:
        # 地址拼接
        file_paths = os.path.join (file_path, file_name)
        # 保存接收的图片到指定根目录
        upload_file.save (file_paths)
    # 这个是图片的访问路径，需返回前端（可有可无）
    url = 'http://192.168.0.108:8000/images/'  # API地址（开启一个8000端口的静态资源服务器）
    image_url = url + file_name
    # 返回图片路径 到前端
    return jsonify ({'code': 0, 'url': image_url, 'imgname': file_name})
