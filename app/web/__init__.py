#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2019/12/31 22:18.
"""

# 蓝图 blueprint 蓝本
# __name__代表蓝图所在模块
from flask import Blueprint

web = Blueprint ('web', __name__)


from app.web import user
from app.web import product
from app.web import web_mutiple
from app.web import web_single
from app.web import inventory
from app.web import category
from app.web import storage
from app.web import record
from app.web import record_product
from app.web import storage_product
