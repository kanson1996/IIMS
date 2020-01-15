#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/7 17:04.
"""

import json

from sqlalchemy import Column, ForeignKey, BigInteger
from sqlalchemy import Integer, Float
from sqlalchemy.orm import relationship

from app.models.base import db, Base


def to_json(inst, cls):
    d = dict ()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr (inst, c.name)
        d[c.name] = v
    return json.dumps (d)


# 库存操作记录商品详情表
class RecordProduct (Base):
    __tablename__ = 'tb_record_product'
    id = Column (BigInteger, primary_key=True, autoincrement=True)
    product_id = Column (Integer, ForeignKey ('product.id'), nullable=False, comment='商品编号')
    change_amount = Column (Integer, nullable=True, comment='商品变更数目（入库、盘点多余则累加，出库、盘点丢失则扣减）')
    price = Column (Float (13), nullable=True, comment='商品采购/销售价格')
    records = relationship ('Record', backref="records")
    record_id = Column (BigInteger, ForeignKey ('record.id'), nullable=True, comment='库存操作记录编号')
    
    __table_args__ = (
        db.UniqueConstraint ('record_id', 'product_id', name='record_id_product_id'),
    )

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
