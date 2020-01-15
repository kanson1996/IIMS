#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/8 21:50.
"""

import json

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models.base import Base


def to_json(inst, cls):
    d = dict ()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr (inst, c.name)
        d[c.name] = v
    return json.dumps (d)


# 仓储信息表
class Storage (Base):
    __tablename__ = 'storage'
    id = Column (Integer, primary_key=True, autoincrement=True, comment='仓储编号')
    storage_name = Column (String (24), nullable=True, comment='仓储名称')
    storage_priority = Column (String (24), nullable=True, comment='仓储优先级')

    @property
    def serialize(self):
        return to_json (self, self.__class__)

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
