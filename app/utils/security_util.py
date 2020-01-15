#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
 Created by Kanson on 2020/1/2 17:32.
"""
import hashlib

# 创建哈希加密函数md5,加密openid，以免暴漏真实id
def md5(data):
    md = hashlib.md5 ()
    md.update (data.encode ('utf-8'))
    data = md.hexdigest ()
    return data