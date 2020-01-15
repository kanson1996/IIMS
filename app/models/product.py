#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/1 23:23.
"""
import json
from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Float
from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.utils.json_util import DateEncoder


def to_json(inst, cls):
    d = dict ()
    '''
    获取表里面的列并存到字典里面
    '''
    for c in cls.__table__.columns:
        v = getattr (inst, c.name)
        d[c.name] = v
    return json.dumps (d, cls=DateEncoder, ensure_ascii=False)


# 商品信息表
class Product (Base):
    __tablename__ = 'product'
    id = Column (Integer, primary_key=True, autoincrement=True, comment='商品编号')
    product_name = Column (String (24), nullable=True, comment='商品名称')
    serial_code = Column (String (24), nullable=True, comment='商品条码')
    factory_price = Column (Float (13), default=0, comment='进货价格')
    sale_price = Column (Float (13), default=0, comment='销售价格')
    manufacturing_date = Column (DateTime (20), default=datetime.now, nullable=True, comment='生产日期')
    shelf_life = Column (String (20), comment='保质期')
    weight = Column (String (20), comment='重量')
    specification = Column (String (20), comment='规格')
    image = Column (String (50), comment='图像')
    sequence = Column (Integer, default=0, comment='商品排序')
    pre_warning_value = Column (Integer, default=0, comment='预警值')
    note = Column (String (50), comment='备注')
    category = relationship ('Category')
    category_id = Column (Integer, ForeignKey ('category.id'), nullable=True)

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


class ResultOfProduct:
    product_id = 0
    product_amount = 0
    category_id = 0
    storage_id = 0
    manufacturing_date = datetime.now ()
    product_name = ''
    sale_price = 0

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
