#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/12 20:26.
"""

import json

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
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


# 商品仓储详情表
class StorageProduct (Base):
    __tablename__ = 'tb_product_storage'
    id = Column (Integer, primary_key=True, autoincrement=True)
    storage_id = Column (Integer, ForeignKey ('storage.id'), nullable=False, comment='仓储编号')
    product_id = Column (Integer, ForeignKey ('product.id'), nullable=False, comment='商品编号')
    product_amount = Column (Integer, nullable=True, default=0, comment='仓储中该商品的当前数目')
    product = relationship ('Product')
    storage = relationship ('Storage')

    __table_args__ = (
        db.UniqueConstraint ('id', 'product_id', name='id_product_id'),
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
