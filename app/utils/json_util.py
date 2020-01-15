#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/2 21:22.
"""
import json
import datetime
import decimal
from sqlalchemy.orm import Query


class AlchemyJsonEncoder (json.JSONEncoder):
    def default(self, obj):
        # 判断是否是Query
        if isinstance (obj, Query):
            # 定义一个字典数组
            fields = []
            # 定义一个字典对象
            record = {}
            # 检索结果集的行记录
            for rec in obj.all ():
                # 检索记录中的成员
                for field in [x for x in dir (rec) if
                              # 过滤属性
                              not x.startswith ('_')
                              # 过滤掉方法属性
                              and hasattr (rec.__getattribute__ (x), '__call__') == False
                              # 过滤掉不需要的属性
                              and x != 'metadata']:
                    data = rec.__getattribute__ (field)
                    try:
                        record[field] = data
                    except TypeError:
                        record[field] = None
                fields.append (record)
            # 返回字典数组
            return fields
        # 其他类型的数据按照默认的方式序列化成JSON
        return json.JSONEncoder.default (self, obj)


class DateEncoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance (obj, datetime.datetime):
            return obj.strftime ("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default (self, obj)


class DecimalEncoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance (obj, decimal.Decimal):
            return float (obj)
        return super (DecimalEncoder, self).default (obj)


class BaseConfig (object):
    RESTFUL_JSON = {'cls': DecimalEncoder}


def dobule_to_dict(self):
    result = {}
    for key in self.__mapper__.c.keys ():
        if getattr (self, key) is not None:
            result[key] = str (getattr (self, key))
        else:
            result[key] = getattr (self, key)
    return result


# 配合todict一起使用
def to_json_str(all_vendors):
    v = [ven.dobule_to_dict () for ven in all_vendors]
    return v


# list 转成Json格式数据
def listToJson(lst):
    import json
    import numpy as np
    keys = [str (x) for x in np.arange (len (lst))]
    list_json = dict (zip (keys, lst))
    str_json = json.dumps (list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json
