#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2019/12/31 22:02.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger

db = SQLAlchemy ()


# 基础Model表
class Base (db.Model):
    __abstract__ = True
    # create_time = Column(DateTime (20), default=datetime.now)
    create_time = Column ('create_time', Integer)
    status = Column (SmallInteger, default=1)

    def __init__(self):
        self.create_time = int (datetime.now ().timestamp ())

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp (self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def set_attrs(self, attrs):
        for key, value in attrs.items ():
            if hasattr (self, key) and key != 'id':
                setattr (self, key, value)
