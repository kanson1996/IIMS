#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/7 17:06.
"""

from flask import request, jsonify

from app.models.base import db
from app.models.category import Category
from app.web import web


@web.route ('/category/add', methods=['GET', 'POST'])
def category_add():
    category = Category ()
    category.category_priority = request.args['priority'] if request.args['priority'] is not None else ''
    category.category_name = request.args['name']
    db.session.add (category)
    db.session.commit ()
    print ('添加成功')
    return jsonify ({'code': 0})


@web.route ('/category/update', methods=['GET', 'POST'])
def category_update():
    id = request.args['id']
    category_name = request.args['name']
    category_priority = request.args['priority']
    category = Category.query.filter_by (id=id).first ()
    category.category_name = category_name
    category.category_priority = category_priority
    db.session.add (category)
    db.session.commit ()
    print ('更新成功')
    return jsonify ({'code': 0})


@web.route ('/category/delete', methods=['GET', 'POST'])
def category_delete():
    id = request.args['id']
    category = Category.query.filter_by (id=id).first ()
    db.session.delete (category)
    db.session.commit ()
    print ('删除成功')
    return jsonify ({'code': 0})


@web.route ('/category/get', methods=['GET', 'POST'])
def category_get_list():
    category_list = db.session.query (Category).filter ().all ()
    print (db.session.query (Category))
    category_json_list = Category.to_json_str (category_list)
    print (category_list)
    print (category_json_list)
    print ('列表返回成功')
    category_name_id = {}
    for category in category_list:
        category_name_id[category.id] = category.category_name
        print (category.id, category.category_name)
    print (category_name_id)
    return jsonify ({'result': {'categoryList': category_json_list, 'categoryKV': category_name_id}})


@web.route ('/category/search', methods=['GET', 'POST'])
def category_search():
    id = request.args['id']
    print ("id:" + id)
    category = Category.query.filter_by (id=id).first ()
    return jsonify ({'result': {'id': id, 'name': category.category_name, 'priority': category.category_priority}})


# 模糊搜索
@web.route ('/category/searchByKey', methods=['GET', 'POST'])
def category_search_by_key():
    keywords = request.args['keywords']
    print ("keywords:" + keywords)
    category_list = Category.query.filter (
        Category.category_name.like ("%" + keywords + "%") if keywords is not None else "").all ()
    category_json_list = Category.to_json_str (category_list)
    return jsonify ({'result': category_json_list})
