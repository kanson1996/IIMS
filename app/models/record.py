#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/10 14:25.
"""
import json
from datetime import datetime

from sqlalchemy import Column, BigInteger
from sqlalchemy import Integer, Float
from sqlalchemy import String, DateTime

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


# 出入库盘点操作记录表
class Record (Base):
    __tablename__ = 'record'
    id = Column (BigInteger, primary_key=True, autoincrement=True, comment='库存操作记录编号')
    storage_id = Column (Integer, nullable=True, comment='仓库ID')
    operate_date = Column (DateTime (20), default=datetime.now, nullable=True, comment='采购/销售/盘点日期')
    operate_person = Column (String (24), nullable=True, comment='操作人员')
    operate_flag = Column (Integer, nullable=True, comment='操作标识（0入库，1出库，2盘点）')
    total_amount = Column (Float (13), nullable=True, comment='商品总价/原盈亏额')
    discount_price = Column (Float (13), nullable=True, comment='折扣价格')
    actual_amount = Column (Float (13), nullable=True, comment='应付/应收总价/实际盈亏额')
    note = Column (String (50), nullable=True, comment='备注')

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
