#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2019/12/31 22:03.
"""

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import Integer, Float
from sqlalchemy import String, DateTime, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base


# 用户信息表
class User (UserMixin, Base):
    __tablename__ = 'user'

    id = Column (Integer, primary_key=True)
    nickname = Column (String (24), nullable=False)
    phone_number = Column (String (18), unique=True)
    confirmed = Column (Boolean, default=False)
    beans = Column (Float, default=0)
    last_time = Column (DateTime (20), nullable=True)
    locked = Column (Boolean, default=False)
    _password = Column ('password', String (128), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash (raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash (self._password, raw)
